#!/usr/bin/env node

/**
 * Performance Baseline Capture Script
 *
 * This script automates performance metric collection using Playwright browser automation.
 *
 * WHAT IT DOES:
 * - Reads performance scenarios from a local configuration file (.claude/performance-config.md)
 * - Launches a headless Chromium browser in your local environment
 * - Navigates to localhost URLs (with port numbers) specified in the configuration
 * - Collects standard browser performance metrics using Web APIs:
 *   - Navigation Timing API (LCP, FCP, DOM Interactive, Total Load Time)
 *   - Resource Timing API (scripts, stylesheets, images, fetch requests)
 * - Runs multiple iterations per scenario (with warmup runs)
 * - Outputs aggregated metrics as JSON to stdout
 *
 * PREREQUISITES:
 * - Node.js >= 16 must be installed in your local environment
 * - @playwright/test package must be installed (npm install -D @playwright/test)
 * - Playwright browsers must be installed (npx playwright install chromium)
 * - Your application must be running locally on the configured port
 *
 * SECURITY:
 * - Only navigates to localhost URLs (127.0.0.0/8, ::1)
 * - Config file must be within current directory (no path traversal)
 * - Port numbers are required and validated (1-65535)
 * - Iterations and warmup runs are bounded (max 50 iterations, 10 warmups)
 * - No remote code execution or untrusted input execution
 * - No credential storage or transmission
 * - Runs entirely in your local Node.js environment
 * - Query strings are stripped from resource URLs before output (prevents token leakage)
 *
 * USAGE:
 *   node capture-baseline.mjs --config path/to/performance-config.md [--port 3000]
 *
 * The --port argument is optional if URLs in the config already include port numbers.
 */

import { chromium } from '@playwright/test';
import { readFile, realpath } from 'fs/promises';
import { URL } from 'url';
import { resolve, relative, isAbsolute } from 'path';
import { spawn } from 'child_process';

// Module-level variables (initialized in validateAndRun)
let configPath;
let portOverride;
let captureMode;

/**
 * Parse performance configuration from markdown file
 * Extracts scenarios table from the Performance Scenarios section
 */
async function parseConfig(configPath) {
  const content = await readFile(configPath, 'utf-8');

  // Extract Performance Scenarios section
  const scenariosMatch = content.match(/## Performance Scenarios[\s\S]*?\n\n([\s\S]*?)(?=\n##|$)/);
  if (!scenariosMatch) {
    throw new Error('Performance Scenarios section not found in configuration');
  }

  const sectionContent = scenariosMatch[1];
  const lines = sectionContent.split('\n');

  // Filter to only actual table rows:
  // - First non-whitespace character is |
  // - Contains at least 4 | characters (for | name | path | description | format)
  const tableLines = lines.filter(line => {
    const trimmed = line.trim();
    return trimmed.startsWith('|') && (trimmed.match(/\|/g) || []).length >= 4;
  });

  if (tableLines.length < 2) {
    throw new Error('Performance Scenarios table not found or incomplete (need at least header + separator rows)');
  }

  // Skip header row (index 0) and separator row (index 1), parse data rows
  const scenarios = [];
  for (let i = 2; i < tableLines.length; i++) {
    const cells = tableLines[i].split('|').map(cell => cell.trim()).filter(Boolean);
    if (cells.length >= 3) {
      scenarios.push({
        name: cells[0],
        path: cells[1],
        description: cells[2]
      });
    }
  }

  // Extract baseline capture settings with bounds
  const settingsMatch = content.match(/## Baseline Capture Settings[\s\S]*?\| Iterations \| (\d+)/);
  const warmupMatch = content.match(/## Baseline Capture Settings[\s\S]*?\| Warmup Runs \| (\d+)/);

  const iterationsRaw = settingsMatch ? parseInt(settingsMatch[1], 10) : 20;
  const warmupRaw = warmupMatch ? parseInt(warmupMatch[1], 10) : 2;

  // Bound iterations to prevent DoS (max 50 iterations, 10 warmup runs)
  const iterations = Math.min(Math.max(iterationsRaw, 1), 50);
  const warmupRuns = Math.min(Math.max(warmupRaw, 0), 10);

  if (iterations !== iterationsRaw) {
    console.error(`Warning: Iterations capped at 50 (config specified ${iterationsRaw})`);
  }
  if (warmupRuns !== warmupRaw) {
    console.error(`Warning: Warmup runs capped at 10 (config specified ${warmupRaw})`);
  }

  return { scenarios, iterations, warmupRuns };
}

/**
 * Validate that URL is localhost only with port (security check)
 */
function validateLocalhostUrl(urlPath, defaultPort) {
  let fullUrl;

  // Validate path before construction - only allow safe path characters to prevent URL injection
  const pathPattern = /^[a-zA-Z0-9\/_\-.:?&=%]+$/;
  if (!urlPath.startsWith('http://') && !urlPath.startsWith('https://') && !pathPattern.test(urlPath)) {
    throw new Error(`Invalid characters in URL path: ${urlPath}. Only alphanumeric, /, _, -, ., :, ?, &, =, % allowed.`);
  }

  // If URL is already complete (starts with http://), validate it
  if (urlPath.startsWith('http://') || urlPath.startsWith('https://')) {
    fullUrl = urlPath;
  } else {
    // Construct URL with localhost and port
    if (!defaultPort) {
      throw new Error(`URL "${urlPath}" does not include a port number. Please specify port in the URL (e.g., "http://localhost:3000/path") or use --port argument.`);
    }
    fullUrl = `http://localhost:${defaultPort}${urlPath.startsWith('/') ? '' : '/'}${urlPath}`;
  }

  try {
    const parsed = new URL(fullUrl);
    const hostname = parsed.hostname.toLowerCase();

    // FIX: Validate pathname characters even for full URLs
    const pathPattern = /^[a-zA-Z0-9\/_\-.:?&=%]+$/;
    if (parsed.pathname && !pathPattern.test(parsed.pathname)) {
      throw new Error(`Invalid characters in URL pathname: ${parsed.pathname}. Only alphanumeric, /, _, -, ., :, ?, &, =, % allowed.`);
    }

    // Comprehensive localhost validation
    // Allow: 'localhost', 127.0.0.0/8 CIDR, ::1
    // Block: 0.0.0.0 (all interfaces), IPv6-mapped IPv4 loopback, any other hostname

    const isLocalhost = hostname === 'localhost';
    const isIPv4Loopback = /^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(hostname);
    const isIPv6Loopback = hostname === '[::1]' || hostname === '::1';

    // Explicitly block dangerous patterns
    const isZeroAddress = hostname === '0.0.0.0';
    const isIPv6Mapped = hostname.includes('::ffff:');

    if (isZeroAddress) {
      throw new Error(`Security: 0.0.0.0 is not allowed (binds to all interfaces). Use localhost or 127.0.0.1.`);
    }

    if (isIPv6Mapped) {
      throw new Error(`Security: IPv6-mapped IPv4 addresses are not allowed. Use localhost or 127.0.0.1.`);
    }

    if (!isLocalhost && !isIPv4Loopback && !isIPv6Loopback) {
      throw new Error(`Security: Only localhost URLs are allowed. Got: ${hostname}`);
    }

    // Validate port exists
    if (!parsed.port) {
      throw new Error(`Port number is required in URL: ${fullUrl}. Use --port argument or include port in URL.`);
    }

    return fullUrl;
  } catch (error) {
    if (error.message.includes('Security:') || error.message.includes('Port number is required') || error.message.includes('Invalid characters')) {
      throw error;
    }
    throw new Error(`Invalid URL: ${urlPath} - ${error.message}`);
  }
}

/**
 * Strip query strings from URLs to prevent token leakage
 */
function stripQueryString(url) {
  try {
    const parsed = new URL(url);
    return `${parsed.origin}${parsed.pathname}`;
  } catch {
    // If URL parsing fails, return as-is (shouldn't happen with resource.name)
    return url;
  }
}

/**
 * Collect performance metrics from browser APIs
 */
async function collectMetrics(page) {
  return await page.evaluate(() => {
    const perfData = {};

    // Navigation Timing API
    const navigation = performance.getEntriesByType('navigation')[0];
    if (navigation) {
      perfData.navigationTiming = {
        dns: navigation.domainLookupEnd - navigation.domainLookupStart,
        tcp: navigation.connectEnd - navigation.connectStart,
        request: navigation.responseStart - navigation.requestStart,
        response: navigation.responseEnd - navigation.responseStart,
        domProcessing: navigation.domComplete - navigation.domInteractive,
        loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
        totalTime: navigation.loadEventEnd - navigation.fetchStart
      };
    }

    // Core Web Vitals
    const paintEntries = performance.getEntriesByType('paint');
    perfData.fcp = paintEntries.find(e => e.name === 'first-contentful-paint')?.startTime || null;

    const lcpEntries = performance.getEntriesByType('largest-contentful-paint');
    perfData.lcp = lcpEntries.length > 0
      ? lcpEntries[lcpEntries.length - 1].startTime
      : null;

    // DOM Interactive time — the point where the browser has parsed all HTML and
    // the DOM is ready, but subresources (scripts, stylesheets) may still be loading.
    // This is NOT Lighthouse TTI. For true TTI, use Lighthouse CLI separately.
    perfData.domInteractive = navigation ? navigation.domInteractive : null;

    // Resource Timing API
    const resources = performance.getEntriesByType('resource');
    perfData.resources = resources.map(resource => ({
      name: resource.name, // Will be sanitized by stripQueryString after collection
      type: resource.initiatorType,
      duration: resource.duration,
      size: resource.transferSize || 0,
      startTime: resource.startTime
    }));

    // Categorize resources by type
    perfData.resourceSummary = {
      scripts: resources.filter(r => r.initiatorType === 'script').length,
      stylesheets: resources.filter(r => r.initiatorType === 'link' || r.initiatorType === 'css').length,
      images: resources.filter(r => r.initiatorType === 'img').length,
      fetch: resources.filter(r => r.initiatorType === 'fetch' || r.initiatorType === 'xmlhttprequest').length,
      total: resources.length
    };

    return perfData;
  });
}

/**
 * Run performance measurement for a single scenario
 */
async function measureScenario(browser, scenario, iterations, warmupRuns, defaultPort) {
  const url = validateLocalhostUrl(scenario.path, defaultPort);
  const allMetrics = [];

  for (let i = 0; i < iterations + warmupRuns; i++) {
    // New context per iteration = isolated cache (true cold-start)
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
      // 'networkidle' waits until no network requests for 500ms — required for SPAs
      // that fetch data after DOMContentLoaded/load events
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

      // Collect metrics
      const metrics = await collectMetrics(page);

      // Strip query strings from resource URLs before storing (prevent token leakage)
      if (metrics.resources) {
        metrics.resources = metrics.resources.map(resource => ({
          ...resource,
          name: stripQueryString(resource.name)
        }));
      }

      // Skip warmup runs
      if (i >= warmupRuns) {
        allMetrics.push(metrics);
      }
    } catch (error) {
      console.error(`Error measuring ${scenario.name} (iteration ${i + 1}): ${error.message}`);
    } finally {
      await context.close(); // Closes page and clears cache
    }
  }

  return aggregateMetrics(allMetrics);
}

/**
 * Aggregate metrics across iterations (mean, p50, p95, p99)
 */
function aggregateMetrics(metricsArray) {
  if (metricsArray.length === 0) {
    return null;
  }

  const aggregate = {
    iterations: metricsArray.length,
    fcp: calculateStats(metricsArray.map(m => m.fcp).filter(v => v !== null)),
    lcp: calculateStats(metricsArray.map(m => m.lcp).filter(v => v !== null)),
    domInteractive: calculateStats(metricsArray.map(m => m.domInteractive).filter(v => v !== null)),
    totalTime: calculateStats(metricsArray.map(m => m.navigationTiming?.totalTime).filter(v => v !== null && v !== undefined)),
    resourceCount: calculateStats(metricsArray.map(m => m.resources?.length || 0)),
    resources: categorizeResources(metricsArray)
  };

  return aggregate;
}

/**
 * Calculate statistical metrics (mean, p50, p95, p99)
 */
function calculateStats(values) {
  if (values.length === 0) return null;

  const sorted = values.slice().sort((a, b) => a - b);
  const sum = values.reduce((a, b) => a + b, 0);

  return {
    mean: Math.round(sum / values.length * 100) / 100,
    p50: sorted[Math.floor(sorted.length * 0.5)],
    p95: sorted[Math.floor(sorted.length * 0.95)],
    p99: sorted[Math.floor(sorted.length * 0.99)]
  };
}

/**
 * Categorize resources by type and preserve individual items
 * Returns: { scripts: { count, items }, stylesheets: { count, items }, ... }
 */
function categorizeResources(metricsArray) {
  // Collect all resources from all iterations
  const allResources = metricsArray.flatMap(m => m.resources || []);

  // Group by type
  const scripts = allResources.filter(r => r.type === 'script');
  const stylesheets = allResources.filter(r => r.type === 'link' || r.type === 'css');
  const images = allResources.filter(r => r.type === 'img');
  const fetch = allResources.filter(r => r.type === 'fetch' || r.type === 'xmlhttprequest');

  // Calculate average metrics per resource (across iterations)
  const avgResources = (resources) => {
    const grouped = {};
    resources.forEach(r => {
      if (!grouped[r.name]) {
        grouped[r.name] = { durations: [], sizes: [], startTimes: [] };
      }
      grouped[r.name].durations.push(r.duration);
      grouped[r.name].sizes.push(r.size);
      grouped[r.name].startTimes.push(r.startTime);
    });

    return Object.entries(grouped).map(([name, data]) => ({
      name,
      duration: Math.round(data.durations.reduce((a, b) => a + b, 0) / data.durations.length),
      size: Math.round(data.sizes.reduce((a, b) => a + b, 0) / data.sizes.length),
      startTime: Math.round(data.startTimes.reduce((a, b) => a + b, 0) / data.startTimes.length)
    }));
  };

  return {
    scripts: { count: Math.round(scripts.length / metricsArray.length), items: avgResources(scripts) },
    stylesheets: { count: Math.round(stylesheets.length / metricsArray.length), items: avgResources(stylesheets) },
    images: { count: Math.round(images.length / metricsArray.length), items: avgResources(images) },
    fetch: { count: Math.round(fetch.length / metricsArray.length), items: avgResources(fetch) }
  };
}

/**
 * Calculate aggregate stats across all scenarios
 */
function calculateCrossScenarioAggregate(scenarios) {
  const allLcp = scenarios.flatMap(s => s.metrics.lcp ? [s.metrics.lcp.mean, s.metrics.lcp.p50, s.metrics.lcp.p95, s.metrics.lcp.p99] : []);
  const allFcp = scenarios.flatMap(s => s.metrics.fcp ? [s.metrics.fcp.mean, s.metrics.fcp.p50, s.metrics.fcp.p95, s.metrics.fcp.p99] : []);
  const allDomInteractive = scenarios.flatMap(s => s.metrics.domInteractive ? [s.metrics.domInteractive.mean, s.metrics.domInteractive.p50, s.metrics.domInteractive.p95, s.metrics.domInteractive.p99] : []);
  const allTotalTime = scenarios.flatMap(s => s.metrics.totalLoadTime ? [s.metrics.totalLoadTime.mean, s.metrics.totalLoadTime.p50, s.metrics.totalLoadTime.p95, s.metrics.totalLoadTime.p99] : []);

  return {
    lcp: calculateStats(allLcp),
    fcp: calculateStats(allFcp),
    domInteractive: calculateStats(allDomInteractive),
    totalLoadTime: calculateStats(allTotalTime)
  };
}

/**
 * Main execution
 */
async function main() {
  let browser;

  try {
    // Parse configuration
    console.error('Checking prerequisites...');
    const config = await parseConfig(configPath);

    if (config.scenarios.length === 0) {
      console.error('No performance scenarios found in configuration');
      process.exit(1);
    }

    // Validate iteration count for statistical rigor
    if (config.iterations < 21) {
      console.error(`Warning: ${config.iterations} iterations is too few for reliable p95 statistics.`);
      console.error('  Recommendation: Use at least 21 iterations for stable p95 measurements.');
      console.error('  With fewer iterations, p95 may not be statistically meaningful.');
      console.error('');
    }

    let results = Object.create(null);

    // Cold-start mode execution
    console.error('Launching Chromium browser (headless)...');
    browser = await chromium.launch({ headless: true });

      for (const scenario of config.scenarios) {
        console.error(`Measuring: ${scenario.name}...`);

        // Sanitize scenario name to prevent prototype pollution
        const safeName = String(scenario.name).replace(/[^a-zA-Z0-9_\- ]/g, '_');

        if (safeName !== scenario.name) {
          console.error(`  Warning: Scenario name sanitized: "${scenario.name}" -> "${safeName}"`);
        }

        results[safeName] = await measureScenario(browser, scenario, config.iterations, config.warmupRuns, portOverride);
      }

    // Build scenarios array with full structure
    const scenarios = [];
    for (const scenario of config.scenarios) {
      const safeName = String(scenario.name).replace(/[^a-zA-Z0-9_\- ]/g, '_');
      const scenarioResult = results[safeName];

      if (scenarioResult) {
        scenarios.push({
          name: safeName,
          url: validateLocalhostUrl(scenario.path, portOverride),
          metrics: {
            lcp: scenarioResult.lcp,
            fcp: scenarioResult.fcp,
            domInteractive: scenarioResult.domInteractive,
            totalLoadTime: scenarioResult.totalTime
          },
          resources: scenarioResult.resources
        });
      }
    }

    // Calculate cross-scenario aggregate
    const aggregate = calculateCrossScenarioAggregate(scenarios);

    // Output JSON results in expected structure
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      mode: captureMode,
      config: {
        iterations: config.iterations,
        warmupRuns: config.warmupRuns,
        port: portOverride
      },
      scenarios: scenarios,
      aggregate: aggregate
    }, null, 2));

  } catch (error) {
    console.error(`Fatal error: ${error.message}`);
    console.error('');
    console.error('Prerequisites checklist:');
    console.error('  1. Is your application running locally?');
    console.error('  2. Is @playwright/test installed? (npm install -D @playwright/test)');
    console.error('  3. Are Playwright browsers installed? (npx playwright install chromium)');
    console.error('  4. Do URLs in your config include port numbers or did you use --port?');
    console.error('  5. Is the config file within the current directory?');
    process.exit(1);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

/**
 * Validate arguments and configuration path, then run main
 * FIX: Includes symlink resolution to prevent path traversal bypass
 */
async function validateAndRun() {
  // Parse command line arguments
  const args = process.argv.slice(2);
  const configIndex = args.indexOf('--config');
  if (configIndex === -1 || !args[configIndex + 1]) {
    console.error('Usage: node capture-baseline.mjs --config <path> [--port <port>] [--mode cold-start]');
    console.error('');
    console.error('Example:');
    console.error('  node capture-baseline.mjs --config .claude/performance-config.md --port 3000');
    console.error('');
    console.error('Prerequisites:');
    console.error('  - Node.js >= 16');
    console.error('  - @playwright/test installed (npm install -D @playwright/test)');
    console.error('  - Playwright browsers installed (npx playwright install chromium)');
    console.error('  - Application running locally on configured port');
    process.exit(1);
  }

  // Validate config path (prevent path traversal)
  const configPathInput = args[configIndex + 1];
  const configPathResolved = resolve(configPathInput);
  const relPath = relative(process.cwd(), configPathResolved);

  if (relPath.startsWith('..') || isAbsolute(relPath)) {
    console.error('Security Error: Config path must be within the current directory');
    console.error(`  Provided: ${configPathInput}`);
    console.error(`  Resolved: ${configPathResolved}`);
    console.error(`  Relative: ${relPath}`);
    process.exit(1);
  }

  // FIX: Resolve symlinks and re-validate
  try {
    const realConfigPath = await realpath(configPathResolved);
    const realRelPath = relative(process.cwd(), realConfigPath);

    if (realRelPath.startsWith('..') || isAbsolute(realRelPath)) {
      console.error('Security Error: Config path symlink points outside current directory');
      console.error(`  Provided: ${configPathInput}`);
      console.error(`  Symlink target: ${realConfigPath}`);
      console.error(`  Relative: ${realRelPath}`);
      process.exit(1);
    }

    // Use the real path (symlink resolved)
    configPath = realConfigPath;
  } catch (error) {
    if (error.code !== 'ENOENT') {
      console.error(`Error resolving config path: ${error.message}`);
      process.exit(1);
    }
    // If file doesn't exist, parseConfig will handle it
    configPath = configPathResolved;
  }

  // Optional port override with validation
  const portIndex = args.indexOf('--port');
  portOverride = null;
  if (portIndex !== -1) {
    const portValue = args[portIndex + 1];
    const portNum = parseInt(portValue, 10);
    if (isNaN(portNum) || portNum < 1 || portNum > 65535) {
      console.error(`Invalid port: ${portValue}. Must be between 1 and 65535.`);
      process.exit(1);
    }
    portOverride = portNum;
  }

  // Mode parameter with validation
  const modeIndex = args.indexOf('--mode');
  captureMode = 'cold-start'; // default
  if (modeIndex !== -1) {
    const modeValue = args[modeIndex + 1];
    if (modeValue !== 'cold-start') {
      console.error(`Invalid mode: ${modeValue}. Only 'cold-start' mode is supported.`);
      process.exit(1);
    }
    captureMode = modeValue;
  }

  // Call main after validation
  await main();
}

validateAndRun();
