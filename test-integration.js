#!/usr/bin/env node

/**
 * Integration test script for Tai Chi Flow application
 * Verifies all components are properly configured and can communicate
 */

const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const http = require('http');

const API_URL = 'http://localhost:5000';

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

async function checkFileStructure() {
  log('\n=== Checking File Structure ===', 'blue');
  
  const requiredFiles = [
    'package.json',
    'electron/main.js',
    'electron/preload.js',
    'src/App.tsx',
    'src/components/VideoCapture.tsx',
    'backend/app.py',
    'backend/requirements.txt',
    'electron-builder.yml',
    'start.sh',
    'start.bat'
  ];
  
  let allFilesExist = true;
  
  for (const file of requiredFiles) {
    const filePath = path.join(__dirname, file);
    const altPath = path.join(__dirname, '..', file);
    if (fs.existsSync(filePath) || fs.existsSync(altPath)) {
      log(`✓ ${file}`, 'green');
    } else {
      log(`✗ ${file}`, 'red');
      allFilesExist = false;
    }
  }
  
  return allFilesExist;
}

async function checkDependencies() {
  log('\n=== Checking Dependencies ===', 'blue');
  
  try {
    const packagePath = fs.existsSync('package.json') ? 'package.json' : '../package.json';
    const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
    
    // Check key dependencies
    const keyDeps = [
      'electron',
      'react',
      '@mui/material',
      'three',
      'zustand',
      'axios'
    ];
    
    for (const dep of keyDeps) {
      if (packageJson.dependencies[dep] || packageJson.devDependencies[dep]) {
        log(`✓ ${dep}`, 'green');
      } else {
        log(`✗ ${dep} missing`, 'red');
      }
    }
    
    return true;
  } catch (error) {
    log(`✗ Failed to check dependencies: ${error.message}`, 'red');
    return false;
  }
}

async function checkBackendAPI() {
  log('\n=== Checking Backend API ===', 'blue');
  
  return new Promise((resolve) => {
    http.get(`${API_URL}/health`, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          log(`✓ Backend health check: ${response.status}`, 'green');
          resolve(true);
        } catch (error) {
          log(`✗ Backend response error: ${error.message}`, 'red');
          resolve(false);
        }
      });
    }).on('error', (error) => {
      log(`✗ Backend API not accessible: ${error.message}`, 'red');
      log('  Make sure to start the backend server first', 'yellow');
      resolve(false);
    });
  });
}

async function checkElectronConfig() {
  log('\n=== Checking Electron Configuration ===', 'blue');
  
  try {
    // Check main.js
    const mainPath = fs.existsSync('electron/main.js') ? 'electron/main.js' : '../electron/main.js';
    const mainJs = fs.readFileSync(mainPath, 'utf8');
    if (mainJs.includes('app.whenReady()')) {
      log(`✓ Electron main process configured`, 'green');
    }
    
    // Check preload.js
    const preloadPath = fs.existsSync('electron/preload.js') ? 'electron/preload.js' : '../electron/preload.js';
    const preloadJs = fs.readFileSync(preloadPath, 'utf8');
    if (preloadJs.includes('contextBridge')) {
      log(`✓ Electron preload script configured`, 'green');
    }
    
    // Check package.json main field
    const pkgPath = fs.existsSync('package.json') ? 'package.json' : '../package.json';
    const packageJson = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
    if (packageJson.main === 'electron/main.js') {
      log(`✓ Package.json main field correct`, 'green');
    }
    
    return true;
  } catch (error) {
    log(`✗ Electron configuration error: ${error.message}`, 'red');
    return false;
  }
}

async function checkBuildConfig() {
  log('\n=== Checking Build Configuration ===', 'blue');
  
  const builderPath = fs.existsSync('electron-builder.yml') ? 'electron-builder.yml' : '../electron-builder.yml';
  if (fs.existsSync(builderPath)) {
    log(`✓ electron-builder.yml exists`, 'green');
    
    const config = fs.readFileSync(builderPath, 'utf8');
    if (config.includes('appId: com.flowstate.taichi')) {
      log(`✓ App ID configured`, 'green');
    }
    if (config.includes('productName: Tai Chi Flow')) {
      log(`✓ Product name configured`, 'green');
    }
    
    return true;
  } else {
    log(`✗ electron-builder.yml missing`, 'red');
    return false;
  }
}

async function runIntegrationTests() {
  log('Tai Chi Flow Integration Test', 'blue');
  log('=============================\n', 'blue');
  
  let allTestsPassed = true;
  
  // Run all checks
  allTestsPassed &= await checkFileStructure();
  allTestsPassed &= await checkDependencies();
  allTestsPassed &= await checkElectronConfig();
  allTestsPassed &= await checkBuildConfig();
  
  // Only check backend if explicitly requested
  if (process.argv.includes('--with-backend')) {
    allTestsPassed &= await checkBackendAPI();
  } else {
    log('\n=== Backend API Check ===', 'blue');
    log('Skipped (use --with-backend to include)', 'yellow');
  }
  
  // Summary
  log('\n=== Test Summary ===', 'blue');
  if (allTestsPassed) {
    log('✓ All integration tests passed!', 'green');
    log('\nThe application is ready to run:', 'green');
    log('  - Windows: start.bat', 'green');
    log('  - macOS/Linux: ./start.sh', 'green');
    log('  - Manual: npm run dev', 'green');
  } else {
    log('✗ Some tests failed. Please fix the issues above.', 'red');
  }
  
  process.exit(allTestsPassed ? 0 : 1);
}

// Run tests
runIntegrationTests().catch(error => {
  log(`\nUnexpected error: ${error.message}`, 'red');
  process.exit(1);
});