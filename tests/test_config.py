import pytest
import os
import json
from src.utils.config import load_config, save_config, get_default_config, DEFAULT_CONFIG

CONFIG_TEST_PATH = "test_config.json"

@pytest.fixture(autouse=True)
def cleanup_test_config():
    """Ensure test_config.json is removed before and after each test."""
    if os.path.exists(CONFIG_TEST_PATH):
        os.remove(CONFIG_TEST_PATH)
    yield
    if os.path.exists(CONFIG_TEST_PATH):
        os.remove(CONFIG_TEST_PATH)

def test_load_config_non_existent():
    """Test loading config when file does not exist, should return default."""
    config = load_config(CONFIG_TEST_PATH)
    assert config == DEFAULT_CONFIG

def test_save_and_load_config():
    """Test saving a config and then loading it."""
    custom_config = {
        "tts": {"rate": 150, "volume": 0.8, "pitch": 1.2, "voice_id": "test_voice"},
        "sentiment_thresholds": {"positive": 0.2, "negative": -0.2}
    }
    save_config(custom_config, CONFIG_TEST_PATH)
    assert os.path.exists(CONFIG_TEST_PATH)
    
    loaded_config = load_config(CONFIG_TEST_PATH)
    assert loaded_config == custom_config

def test_get_default_config():
    """Test that get_default_config returns a copy of DEFAULT_CONFIG."""
    default_copy = get_default_config()
    assert default_copy == DEFAULT_CONFIG
    assert id(default_copy) != id(DEFAULT_CONFIG) # Ensure it's a copy

def test_save_config_creates_directory():
    """Test that save_config creates directory if it doesn't exist."""
    nested_path = "temp_dir/nested_config.json"
    if os.path.exists("temp_dir"):
        import shutil
        shutil.rmtree("temp_dir") # Clean up if exists from previous failed run

    custom_config = {"key": "value"}
    save_config(custom_config, nested_path)
    assert os.path.exists(nested_path)
    
    # Cleanup
    if os.path.exists("temp_dir"):
        import shutil
        shutil.rmtree("temp_dir")

def test_load_config_invalid_json():
    """Test loading an invalid JSON file, should return default config."""
    with open(CONFIG_TEST_PATH, 'w') as f:
        f.write("this is not json")
    
    # load_config should handle JSON errors gracefully and return default
    config = load_config(CONFIG_TEST_PATH)
    assert config == DEFAULT_CONFIG
