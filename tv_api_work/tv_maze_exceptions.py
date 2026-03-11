""" TV Maze API exception classes."""


class BaseError(Exception):
    """Base exception class for all TV Maze errors."""

    def __init__(self, value):
        super().__init__(value)
        self.value = value

    def __str__(self):
        return self.value


class ShowNotFound(BaseError):
    """Raised when a TV show cannot be found."""


class IDNotFound(BaseError):
    """Raised when a maze ID cannot be found."""


class ScheduleNotFound(BaseError):
    """Raised when a schedule cannot be found."""


class EpisodeNotFound(BaseError):
    """Raised when an episode cannot be found."""


class NoEpisodesForAirdate(BaseError):
    """Raised when no episodes exist for a given airdate."""


class CastNotFound(BaseError):
    """Raised when cast information cannot be found."""


class ShowIndexError(BaseError):
    """Raised when a show index error occurs."""


class PersonNotFound(BaseError):
    """Raised when a person cannot be found."""


class CreditsNotFound(BaseError):
    """Raised when credits cannot be found."""


class UpdateNotFound(BaseError):
    """Raised when an update cannot be found."""


class AKASNotFound(BaseError):
    """Raised when AKAs cannot be found."""


class SeasonNotFound(BaseError):
    """Raised when a season cannot be found."""


class GeneralError(BaseError):
    """Raised for general TV Maze errors."""


class MissingParameters(BaseError):
    """Raised when required parameters are missing."""


class IllegalAirDate(BaseError):
    """Raised when an air date is invalid."""


class TvMazeConnectionError(BaseError):
    """Raised when a connection error occurs. Renamed to avoid shadowing built-in."""


class BadRequest(BaseError):
    """Raised when a bad request is made to the API."""


class NoFollowedShows(BaseError):
    """Raised when there are no followed shows."""


class ShowNotFollowed(BaseError):
    """Raised when a show is not being followed."""


class NoFollowedPeople(BaseError):
    """Raised when there are no followed people."""


class PersonNotFollowed(BaseError):
    """Raised when a person is not being followed."""


class NoMarkedEpisodes(BaseError):
    """Raised when there are no marked episodes."""


class EpisodeNotMarked(BaseError):
    """Raised when an episode is not marked."""


class InvalidMarkedEpisodeType(BaseError):
    """Raised when a marked episode type is invalid."""


class InvalidEmbedValue(BaseError):
    """Raised when an embed value is invalid."""


class NetworkNotFollowed(BaseError):
    """Raised when a network is not being followed."""


class NoFollowedWebChannels(BaseError):
    """Raised when there are no followed web channels."""


class NoVotedShows(BaseError):
    """Raised when there are no voted shows."""


class ShowNotVotedFor(BaseError):
    """Raised when a show has not been voted for."""


class InvalidVoteValue(BaseError):
    """Raised when a vote value is invalid."""


class NoVotedEpisodes(BaseError):
    """Raised when there are no voted episodes."""


class EpisodeNotVotedFor(BaseError):
    """Raised when an episode has not been voted for."""


class CrewNotFound(BaseError):
    """Raised when crew information cannot be found."""


class NoFollowedNetworks(BaseError):
    """Raised when there are no followed networks."""


class NetworkNotFound(BaseError):
    """Raised when a network cannot be found."""


class WebChannelNotFound(BaseError):
    """Raised when a web channel cannot be found."""


class WebChannelNotFollowed(BaseError):
    """Raised when a web channel is not being followed."""
