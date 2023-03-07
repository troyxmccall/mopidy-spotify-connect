from unittest import mock
from unittest.mock import sentinel

import pytest
from mopidy import audio
from mopidy import backend as backend_api

from mopidy_spotify import backend


@pytest.fixture
def audio_mock():
    audio_mock = mock.Mock(spec=audio.Audio)
    return audio_mock


@pytest.fixture
def backend_mock(config):
    backend_mock = mock.Mock(spec=backend.SpotifyBackend)
    backend_mock._config = config
    return backend_mock


@pytest.fixture
def provider(audio_mock, backend_mock):
    return backend.SpotifyPlaybackProvider(
        audio=audio_mock, backend=backend_mock
    )


def test_is_a_playback_provider(provider):
    assert isinstance(provider, backend_api.PlaybackProvider)


def test_on_source_setup_sets_properties(config, provider):
    mock_source = mock.MagicMock()
    provider._cache_location = sentinel.cache_dir
    provider.on_source_setup(mock_source)

    assert mock_source.set_property.mock_calls == [
        mock.call("username", "alice"),
        mock.call("password", "password"),
        mock.call("bitrate", 160),
        mock.call("cache-credentials", sentinel.cache_dir),
        mock.call("cache-files", sentinel.cache_dir),
    ]


def test_on_source_setup_without_caching(config, provider):
    config["spotify"]["allow_cache"] = False
    mock_source = mock.MagicMock()
    provider.on_source_setup(mock_source)

    assert mock_source.set_property.mock_calls == [
        mock.call("username", "alice"),
        mock.call("password", "password"),
        mock.call("bitrate", 160),
    ]


def test_on_source_setup_bitrate(config, provider):
    config["spotify"]["bitrate"] = 320
    mock_source = mock.MagicMock()
    provider.on_source_setup(mock_source)

    assert mock.call("bitrate", 320) in mock_source.set_property.mock_calls
