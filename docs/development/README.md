# Development Documentation

This directory contains detailed development guides for each component of the Tai Chi Flow application.

## 📖 Available Guides

### [Backend Development](./backend.md)
- Python/Flask API development
- Video processing pipeline
- Pose detection implementation
- API endpoint reference

### [Frontend Development](./frontend.md)
- React component architecture
- Three.js 3D visualization
- State management with Zustand
- TypeScript patterns

### [Electron Development](./electron.md)
- Desktop application setup
- IPC communication
- Native integrations
- Build and distribution

## 🎯 Quick Start for Developers

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd flowstate

# Install all dependencies
npm install
cd backend && pip install -r requirements.txt
cd ..
```

### 2. Development Mode

```bash
# Run all services concurrently
npm run dev

# Or run individually:
npm run dev:backend   # Python backend
npm run dev:react     # React frontend
npm run dev:electron  # Electron app
```

### 3. Testing

```bash
# Frontend tests
npm test

# Backend tests
npm run test:backend

# Integration tests
node test-integration.js
```

## 🔧 Development Tools

### Recommended IDE Setup

- **VS Code** with extensions:
  - ESLint
  - Prettier
  - Python
  - TypeScript
  - React snippets

### Debugging

- Chrome DevTools for frontend
- Python debugger for backend
- Electron DevTools for desktop

## 📐 Code Standards

### TypeScript/JavaScript
- ESLint configuration
- Prettier formatting
- Strict TypeScript mode

### Python
- PEP 8 compliance
- Type hints
- Docstrings

## 🎯 Architecture Principles

1. **Separation of Concerns**
   - Clear boundaries between layers
   - Minimal coupling
   - Well-defined interfaces

2. **Performance First**
   - Efficient video processing
   - Optimized 3D rendering
   - Smooth user experience

3. **Type Safety**
   - TypeScript for frontend
   - Python type hints
   - Validated API contracts

## 🚀 Deployment

See individual guides for platform-specific build instructions:
- [Building for Production](./electron.md#building--distribution)
- [Backend Deployment](./backend.md#deployment)
- [Frontend Optimization](./frontend.md#performance-optimization)