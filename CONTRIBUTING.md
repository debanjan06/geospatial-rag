# Contributing to GeoSpatial-RAG

Thank you for your interest in contributing to GeoSpatial-RAG! We welcome contributions from the community and are excited to see how you can help improve our framework for remote sensing image analysis.

## 🌟 Ways to Contribute

### 🐛 Bug Reports
- Search existing issues before creating a new one
- Use clear, descriptive titles
- Include steps to reproduce the issue
- Provide system information (OS, Python version, GPU details)
- Include error messages and stack traces

### 💡 Feature Requests
- Check if the feature has already been requested
- Clearly describe the proposed functionality
- Explain the use case and potential benefits
- Consider providing implementation suggestions

### 🔧 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Documentation enhancements
- Test coverage improvements

### 📚 Documentation
- Fix typos and grammatical errors
- Improve existing documentation clarity
- Add examples and tutorials
- Translate documentation to other languages

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- CUDA-compatible GPU (recommended for development)
- Familiarity with PyTorch, CLIP, and LangChain

### Development Setup

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/geospatial-rag.git
   cd geospatial-rag
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/debanjan06/geospatial-rag.git
   ```

4. **Create a virtual environment**
   ```bash
   python -m venv geospatial_env
   
   # Windows
   geospatial_env\Scripts\activate
   
   # Linux/MacOS
   source geospatial_env/bin/activate
   ```

5. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   
   # Install additional development tools
   pip install pytest pytest-cov black flake8 pre-commit
   ```

6. **Set up pre-commit hooks** (optional but recommended)
   ```bash
   pre-commit install
   ```

## 📝 Development Workflow

### Creating a Branch
```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create a feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### Making Changes

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use meaningful variable and function names
   - Add docstrings to functions and classes
   - Keep functions focused and modular

2. **Testing**
   ```bash
   # Run existing tests
   pytest tests/ -v
   
   # Run with coverage
   pytest tests/ --cov=geospatial_rag --cov-report=html
   
   # Test specific modules
   pytest tests/test_embeddings.py
   ```

3. **Adding Tests**
   - Write tests for new functionality
   - Ensure tests cover edge cases
   - Maintain or improve test coverage
   - Place tests in the appropriate `tests/` subdirectory

4. **Documentation**
   - Update docstrings for modified functions
   - Update README.md if necessary
   - Add comments for complex logic
   - Update type hints

### Code Quality Checks
```bash
# Format code with Black
black src/ tests/

# Check code style with Flake8
flake8 src/ tests/

# Run all quality checks
python -m pytest tests/ && black --check src/ tests/ && flake8 src/ tests/
```

### Committing Changes

Use conventional commit messages:
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `test:` adding or updating tests
- `refactor:` code refactoring
- `perf:` performance improvements
- `style:` code style changes

Examples:
```bash
git commit -m "feat: add support for multispectral image processing"
git commit -m "fix: resolve CLIP model loading issue on CPU-only systems"
git commit -m "docs: update installation guide for Windows users"
```

### Submitting a Pull Request

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a pull request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Choose your feature branch
   - Fill out the PR template

3. **PR Guidelines**
   - Use a clear, descriptive title
   - Reference related issues using `#issue_number`
   - Describe what your changes do
   - Include screenshots for UI changes
   - List any breaking changes
   - Ensure all checks pass

## 🧪 Testing Guidelines

### Writing Tests
- Use pytest for all tests
- Follow the AAA pattern (Arrange, Act, Assert)
- Use descriptive test names
- Mock external dependencies when necessary

### Test Structure
```python
def test_feature_functionality():
    """Test that feature works as expected."""
    # Arrange
    input_data = create_test_data()
    expected_output = "expected_result"
    
    # Act
    result = your_function(input_data)
    
    # Assert
    assert result == expected_output
```

### Integration Tests
- Test the complete pipeline end-to-end
- Use small test datasets
- Verify performance benchmarks
- Test error handling scenarios

## 📋 Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows the project's style guidelines
- [ ] All tests pass locally
- [ ] New functionality includes appropriate tests
- [ ] Documentation is updated where necessary
- [ ] Commit messages follow conventional format
- [ ] No merge conflicts with main branch
- [ ] PR description clearly explains the changes
- [ ] Related issues are referenced
- [ ] Breaking changes are documented

## 🎯 Priority Areas for Contribution

We especially welcome contributions in these areas:

### 🔬 Model Integration
- Support for new vision-language models
- Integration with latest CLIP variants
- Custom model architectures for remote sensing

### 📊 Dataset Support
- New remote sensing datasets
- Data preprocessing pipelines
- Annotation tools and utilities

### 🚀 Performance Optimization
- GPU memory optimization
- Batch processing improvements
- Caching mechanisms
- Distributed processing support

### 🌐 User Interface
- Mobile application development
- Desktop GUI applications
- API endpoint development
- Visualization improvements

### 📚 Documentation & Examples
- Tutorial notebooks
- Use case examples
- API documentation
- Video tutorials

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

### Communication
- Use clear, professional language
- Be patient with questions and discussions
- Provide helpful feedback on PRs and issues
- Share knowledge and learning resources

## 🏷️ Issue Labels

We use these labels to organize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to docs
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `performance`: Performance improvements
- `testing`: Related to testing
- `ui/ux`: User interface and experience

## 📞 Getting Help

If you need help or have questions:

1. **Check existing issues and discussions**
2. **Read the documentation thoroughly**
3. **Join our community discussions**
4. **Contact maintainers**: bl.sc.p2dsc24032@bl.students.amrita.edu

### Before Asking for Help
- Search existing issues and documentation
- Provide complete error messages
- Include system information
- Describe what you've already tried

## 🎉 Recognition

Contributors will be:
- Listed in our contributors section
- Mentioned in release notes for significant contributions
- Invited to join our contributor community
- Eligible for maintainer roles based on sustained contributions

## 📜 License

By contributing to GeoSpatial-RAG, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make GeoSpatial-RAG better! Every contribution, no matter how small, makes a difference. 🌍✨
