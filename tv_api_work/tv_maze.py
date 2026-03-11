"""TV Maze API wrapper."""
# pylint: disable=too-many-lines,too-many-instance-attributes,too-few-public-methods
# pylint: disable=missing-class-docstring,missing-function-docstring
# pylint: disable=protected-access,wildcard-import,unused-wildcard-import
# pylint: disable=import-error

import re
from datetime import datetime
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from . import tv_maze_endpoints as endpoints
from .tv_maze_exceptions import *


class Show:
    def __init__(self, data):
        self.status = data.get('status')
        self.rating = data.get('rating')
        self.genres = data.get('genres')
        self.weight = data.get('weight')
        self.updated = data.get('updated')
        self.name = data.get('name')
        self.language = data.get('language')
        self.schedule = data.get('schedule')
        self.url = data.get('url')
        self.image = data.get('image')
        self.externals = data.get('externals')
        self.premiered = data.get('premiered')
        self.summary = _remove_tags(data.get('summary', ''))
        self.links = data.get('_links')
        self.web_channel = WebChannel(data.get('webChannel')) if data.get('webChannel') else None
        self.runtime = data.get('runtime')
        self.type = data.get('type')
        self.id = data.get('id')
        self.maze_id = self.id
        self.network = Network(data.get('network')) if data.get('network') else None
        self.__episodes = []
        self.seasons = {}
        self.cast = None
        self.__nextepisode = None
        self.__previousepisode = None
        self.populate(data)

    def __repr__(self):
        year = str(self.premiered[:4]) if self.premiered else None
        if self.web_channel:
            platform = ',show_web_channel='
            network = self.web_channel.name
        elif self.network:
            platform = ',network='
            network = self.network.name
        else:
            platform = ''
            network = ''
        return (f'<Show(maze_id={self.maze_id},name={self.name},'
                f'year={year}{platform}{network})>')

    def __str__(self):
        return self.name

    def __iter__(self):
        return iter(self.seasons.values())

    def __bool__(self):
        return bool(self.id)

    def __len__(self):
        return len(self.seasons)

    def __getitem__(self, item):
        try:
            return self.seasons[item]
        except KeyError as exc:
            raise SeasonNotFound(
                f'Season {item} does not exist for show {self.name}.') from exc

    @property
    def next_episode(self):
        if (self.__nextepisode is None
                and 'nextepisode' in self.links
                and 'href' in self.links['nextepisode']):
            episode_id = self.links['nextepisode']['href'].rsplit('/', 1)[1]
            if episode_id.isdigit():
                self.__nextepisode = episode_by_id(episode_id)
        return self.__nextepisode

    @property
    def previous_episode(self):
        if (self.__previousepisode is None
                and 'previousepisode' in self.links
                and 'href' in self.links['previousepisode']):
            episode_id = self.links['previousepisode']['href'].rsplit('/', 1)[1]
            if episode_id.isdigit():
                self.__previousepisode = episode_by_id(episode_id)
        return self.__previousepisode

    @property
    def episodes(self):
        if not self.__episodes:
            self.__episodes = episode_list(self.maze_id, specials=True)
        return self.__episodes

    def populate(self, data):
        embedded = data.get('_embedded')
        if embedded:
            if embedded.get('episodes'):
                seasons = show_seasons(self.maze_id)
                for episode in embedded.get('episodes'):
                    self.__episodes.append(Episode(episode))
                for episode in self.__episodes:
                    season_num = int(episode.season_number)
                    if season_num not in self.seasons:
                        self.seasons[season_num] = seasons[season_num]
                        self.seasons[season_num].show = self
                    self.seasons[season_num].episodes[episode.episode_number] = episode
            if embedded.get('cast'):
                self.cast = Cast(embedded.get('cast'))


class Season:
    def __init__(self, data):
        self.show = None
        self.episodes = {}
        self.id = data.get('id')
        self.url = data.get('url')
        self.season_number = data.get('number')
        self.name = data.get('name')
        self.episode_order = data.get('episodeOrder')
        self.premier_date = data.get('premierDate')
        self.end_date = data.get('endDate')
        self.network = Network(data.get('network')) if data.get('network') else None
        self.web_channel = WebChannel(data.get('webChannel')) if data.get('webChannel') else None
        self.image = data.get('image')
        self.summary = data.get('summary')
        self.links = data.get('_links')

    def __repr__(self):
        return f'<Season(id={self.id},season_number={str(self.season_number).zfill(2)})>'

    def __iter__(self):
        return iter(self.episodes.values())

    def __len__(self):
        return len(self.episodes)

    def __getitem__(self, item):
        try:
            return self.episodes[item]
        except KeyError as exc:
            raise EpisodeNotFound(
                f'Episode {item} does not exist for season '
                f'{self.season_number} of show {self.show}.') from exc

    def __bool__(self):
        return bool(self.id)


class Episode:
    def __init__(self, data):
        self.title = data.get('name')
        self.airdate = data.get('airdate')
        self.url = data.get('url')
        self.season_number = data.get('season')
        self.episode_number = data.get('number')
        self.image = data.get('image')
        self.airstamp = data.get('airstamp')
        self.airtime = data.get('airtime')
        self.runtime = data.get('runtime')
        self.summary = _remove_tags(data.get('summary'))
        self.maze_id = data.get('id')
        self.special = self.is_special()
        if data.get('show'):
            self.show = Show(data.get('show'))
        if data.get('_embedded'):
            if data['_embedded'].get('show'):
                self.show = Show(data['_embedded']['show'])

    def __repr__(self):
        epnum = 'Special' if self.special else self.episode_number
        return (f'<Episode(season={str(self.season_number).zfill(2)},'
                f'episode_number={str(epnum).zfill(2)})>')

    def __str__(self):
        season = 'S' + str(self.season_number).zfill(2)
        episode = ' Special' if self.special else 'E' + str(self.episode_number).zfill(2)
        return season + episode + ' ' + self.title

    def is_special(self):
        if self.episode_number:
            return False
        return True


class Person:
    def __init__(self, data):
        if data.get('person'):
            data = data['person']
        self.links = data.get('_links')
        self.id = data.get('id')
        self.image = data.get('image')
        self.name = data.get('name')
        self.score = data.get('score')
        self.url = data.get('url')
        self.character = None
        self.castcredits = None
        self.crewcredits = None
        self.populate(data)

    def populate(self, data):
        if data.get('_embedded'):
            if data['_embedded'].get('castcredits'):
                self.castcredits = [CastCredit(credit)
                                    for credit in data['_embedded']['castcredits']]
            elif data['_embedded'].get('crewcredits'):
                self.crewcredits = [CrewCredit(credit)
                                    for credit in data['_embedded']['crewcredits']]

    def __repr__(self):
        return f'<Person(name={self.name},maze_id={self.id})>'

    def __str__(self):
        return self.name


class Character:
    def __init__(self, data):
        self.id = data.get('id')
        self.url = data.get('url')
        self.name = data.get('name')
        self.image = data.get('image')
        self.links = data.get('_links')
        self.person = None

    def __repr__(self):
        return f'<Character(name={self.name},maze_id={self.id})>'

    def __str__(self):
        return self.name


class Cast:
    def __init__(self, data):
        self.people = []
        self.characters = []
        self.populate(data)

    def populate(self, data):
        for cast_member in data:
            self.people.append(Person(cast_member['person']))
            self.characters.append(Character(cast_member['character']))
            self.people[-1].character = self.characters[-1]
            self.characters[-1].person = self.people[-1]


class CastCredit:
    def __init__(self, data):
        self.links = data.get('_links')
        self.character = None
        self.show = None
        self.populate(data)

    def populate(self, data):
        if data.get('_embedded'):
            if data['_embedded'].get('character'):
                self.character = Character(data['_embedded']['character'])
            elif data['_embedded'].get('show'):
                self.show = Show(data['_embedded']['show'])


class CrewCredit:
    def __init__(self, data):
        self.links = data.get('_links')
        self.type = data.get('type')
        self.show = None
        self.populate(data)

    def populate(self, data):
        if data.get('_embedded'):
            if data['_embedded'].get('show'):
                self.show = Show(data['_embedded']['show'])


class Crew:
    def __init__(self, data):
        self.person = Person(data.get('person'))
        self.type = data.get('type')

    def __repr__(self):
        return (f'<Crew(name={self.person.name},'
                f'maze_id={self.person.id},type={self.type})>')


class Updates:
    def __init__(self, data):
        self.updates = {}
        self.populate(data)

    def populate(self, data):
        for maze_id, time in data.items():
            self.updates[int(maze_id)] = Update(maze_id, time)

    def __getitem__(self, item):
        try:
            return self.updates[item]
        except KeyError as exc:
            raise UpdateNotFound(f'No update found for Maze id {item}.') from exc

    def __iter__(self):
        return iter(self.updates.values())


class Update:
    def __init__(self, maze_id, time):
        self.maze_id = int(maze_id)
        self.seconds_since_epoch = time
        self.timestamp = datetime.fromtimestamp(time)

    def __repr__(self):
        return f'<Update(maze_id={self.maze_id},time={self.seconds_since_epoch})>'


class AKA:
    def __init__(self, data):
        self.name = data.get('name')
        self.country = data.get('country')

    def __repr__(self):
        return f'<AKA(name={self.name},country={self.country})>'


class Network:
    def __init__(self, data):
        self.name = data.get('name')
        self.maze_id = data.get('id')
        self.country = None
        self.timezone = None
        self.code = None
        if data.get('country'):
            self.country = data['country'].get('name')
            self.timezone = data['country'].get('timezone')
            self.code = data['country'].get('code')

    def __repr__(self):
        return f'<Network(name={self.name},country={self.country})>'


class WebChannel:
    def __init__(self, data):
        self.name = data.get('name')
        self.maze_id = data.get('id')
        self.country = None
        self.timezone = None
        self.code = None
        if data.get('country'):
            self.country = data['country'].get('name')
            self.timezone = data['country'].get('timezone')
            self.code = data['country'].get('code')

    def __repr__(self):
        return f'<WebChannel(name={self.name},country={self.country})>'


class FollowedShow:
    def __init__(self, data):
        self.maze_id = data.get('show_id')
        self.show = None
        if data.get('_embedded'):
            self.show = Show(data['_embedded'].get('show'))

    def __repr__(self):
        return f'<FollowedShow(maze_id={self.maze_id})>'


class FollowedPerson:
    def __init__(self, data):
        self.person_id = data.get('person_id')
        self.person = None
        if data.get('_embedded'):
            self.person = Person(data['_embedded'].get('person'))

    def __repr__(self):
        return f'<FollowedPerson(person_id={self.person_id})>'


class FollowedNetwork:
    def __init__(self, data):
        self.network_id = data.get('network_id')
        self.network = None
        if data.get('_embedded'):
            self.network = Network(data['_embedded'].get('network'))

    def __repr__(self):
        return f'<FollowedNetwork(network_id={self.network_id})>'


class FollowedWebChannel:
    def __init__(self, data):
        self.web_channel_id = data.get('webchannel_id')
        self.web_channel = None
        if data.get('_embedded'):
            self.web_channel = WebChannel(data['_embedded'].get('webchannel'))

    def __repr__(self):
        return f'<FollowedWebChannel(web_channel_id={self.web_channel_id})>'


class MarkedEpisode:
    def __init__(self, data):
        self.episode_id = data.get('episode_id')
        self.marked_at = data.get('marked_at')
        type_ = data.get('type')
        types = {0: 'watched', 1: 'acquired', 2: 'skipped'}
        self.type = types[type_]

    def __repr__(self):
        return (f'<MarkedEpisode(episode_id={self.episode_id},'
                f'marked_at={self.marked_at},type={self.type})>')


class VotedShow:
    def __init__(self, data):
        self.maze_id = data.get('show_id')
        self.voted_at = data.get('voted_at')
        self.vote = data.get('vote')
        if data.get('_embedded'):
            self.show = Show(data['_embedded'].get('show'))

    def __repr__(self):
        return (f'<VotedShow(maze_id={self.maze_id},'
                f'voted_at={self.voted_at},vote={self.vote})>')


class VotedEpisode:
    def __init__(self, data):
        self.episode_id = data.get('episode_id')
        self.voted_at = data.get('voted_at')
        self.vote = data.get('vote')

    def __repr__(self):
        return (f'<VotedEpisode(episode_id={self.episode_id},'
                f'voted_at={self.voted_at},vote={self.vote})>')


# ==================== HELPER FUNCTIONS ====================

def _valid_encoding(text):
    if not text:
        return None
    return text


def _url_quote(show):
    return requests.utils.quote(show.encode('UTF-8'))


def _remove_tags(text):
    if not text:
        return None
    return re.sub(r'<.*?>', '', text)


# ==================== TVMAZE CLASS ====================

class TVMaze:
    """Main class enabling interaction with both free and Premium TVMaze features.

    Attributes:
        username (str): Username for http://www.tvmaze.com
        api_key (str): TVMaze api key. Find your key at http://www.tvmaze.com/dashboard
    """

    def __init__(self, username=None, api_key=None):
        self.username = username
        self.api_key = api_key

    @staticmethod
    def _endpoint_standard_get(url):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[429])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        try:
            r = s.get(url)
        except requests.exceptions.ConnectionError as e:
            raise TvMazeConnectionError(repr(e)) from e
        s.close()
        if r.status_code in [404, 422]:
            return None
        if r.status_code == 400:
            raise BadRequest(f'Bad Request for url {url}')
        return r.json()

    def _endpoint_premium_get(self, url):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[429])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        try:
            r = s.get(url, auth=(self.username, self.api_key))
        except requests.exceptions.ConnectionError as e:
            raise TvMazeConnectionError(repr(e)) from e
        s.close()
        if r.status_code in [404, 422]:
            return None
        if r.status_code == 400:
            raise BadRequest(f'Bad Request for url {url}')
        return r.json()

    def _endpoint_premium_delete(self, url):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[429])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        try:
            r = s.delete(url, auth=(self.username, self.api_key))
        except requests.exceptions.ConnectionError as e:
            raise TvMazeConnectionError(repr(e)) from e
        s.close()
        if r.status_code == 400:
            raise BadRequest(f'Bad Request for url {url}')
        if r.status_code == 200:
            return True
        if r.status_code == 404:
            return None
        return None

    def _endpoint_premium_put(self, url, payload=None):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[429])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        try:
            r = s.put(url, data=payload, auth=(self.username, self.api_key))
        except requests.exceptions.ConnectionError as e:
            raise TvMazeConnectionError(repr(e)) from e
        s.close()
        if r.status_code == 400:
            raise BadRequest(f'Bad Request for url {url}')
        if r.status_code == 200:
            return True
        if r.status_code in [404, 422]:
            return None
        return None

    def get_show(self, maze_id=None, tvdb_id=None, tvrage_id=None, imdb_id=None,
                 show_name=None, show_year=None, show_network=None, show_language=None,
                 show_country=None, show_web_channel=None, embed=None):
        """Get Show object directly via id or indirectly via name + optional qualifiers.

        If only a show_name is given, the show with the highest score using the
        tvmaze algorithm will be returned.
        Args:
            maze_id: Show maze_id
            tvdb_id: Show tvdb_id
            tvrage_id: Show tvrage_id
            show_name: Show name to be searched
            show_year: Show premiere year
            show_network: Show TV Network (like ABC, NBC, etc.)
            show_web_channel: Show Web Channel (like Netflix, Amazon, etc.)
            show_language: Show language
            show_country: Show country
            embed: embed parameter to include additional data
        """
        errors = []
        if not (maze_id or tvdb_id or tvrage_id or imdb_id or show_name):
            raise MissingParameters(
                'Either maze_id, tvdb_id, tvrage_id, imdb_id or show_name '
                'are required to get show, none provided,')
        if maze_id:
            try:
                return show_main_info(maze_id, embed=embed)
            except IDNotFound as e:
                errors.append(e.value)
        if tvdb_id:
            try:
                return show_main_info(lookup_tvdb(tvdb_id).id, embed=embed)
            except IDNotFound as e:
                errors.append(e.value)
        if tvrage_id:
            try:
                return show_main_info(lookup_tvrage(tvrage_id).id, embed=embed)
            except IDNotFound as e:
                errors.append(e.value)
        if imdb_id:
            try:
                return show_main_info(lookup_imdb(imdb_id).id, embed=embed)
            except IDNotFound as e:
                errors.append(e.value)
        if show_name:
            try:
                show = self._get_show_by_search(
                    show_name, show_year, show_network,
                    show_language, show_country, show_web_channel, embed=embed)
                return show
            except ShowNotFound as e:
                errors.append(e.value)
        raise ShowNotFound(' ,'.join(errors))

    def _get_show_with_qualifiers(self, show_name, qualifiers):
        shows = get_show_list(show_name)
        best_match = -1
        show_match = None
        for show in shows:
            premiered = show.premiered[:-6].lower() if show.premiered else None
            network = show.network.name.lower() if show.network and show.network.name else None
            web_channel = (show.web_channel.name.lower()
                           if show.web_channel and show.web_channel.name else None)
            if show.network and show.network.code:
                country = show.network.code.lower()
            elif show.web_channel and show.web_channel.code:
                country = show.web_channel.code.lower()
            else:
                country = None
            language = show.language.lower() if show.language else None
            attributes = [premiered, country, network, language, web_channel]
            show_score = len(set(qualifiers) & set(attributes))
            if show_score > best_match:
                best_match = show_score
                show_match = show
        return show_match

    def _get_show_by_search(self, show_name, show_year, show_network, show_language,
                            show_country, show_web_channel, embed):
        if show_year:
            show_year = str(show_year)
        qualifiers = list(filter(None, [show_year, show_network, show_language,
                                        show_country, show_web_channel]))
        if qualifiers:
            qualifiers = [q.lower() for q in qualifiers if q]
            show = self._get_show_with_qualifiers(show_name, qualifiers)
        else:
            return show_single_search(show=show_name, embed=embed)
        if embed:
            return show_main_info(maze_id=show.id, embed=embed)
        return show

    def get_followed_shows(self, embed=None):
        if embed not in [None, 'show']:
            raise InvalidEmbedValue('Value for embed must be "show" or None')
        url = endpoints.followed_shows.format('/')
        if embed == 'show':
            url = endpoints.followed_shows.format('?embed=show')
        q = self._endpoint_premium_get(url)
        if q:
            return [FollowedShow(show) for show in q]
        raise NoFollowedShows('You have not followed any shows yet')

    def get_followed_show(self, maze_id):
        url = endpoints.followed_shows.format('/' + str(maze_id))
        q = self._endpoint_premium_get(url)
        if q:
            return FollowedShow(q)
        raise ShowNotFollowed(f'Show with ID {maze_id} is not followed')

    def follow_show(self, maze_id):
        url = endpoints.followed_shows.format('/' + str(maze_id))
        q = self._endpoint_premium_put(url)
        if not q:
            raise ShowNotFound(f'Show with ID {maze_id} does not exist')

    def unfollow_show(self, maze_id):
        url = endpoints.followed_shows.format('/' + str(maze_id))
        q = self._endpoint_premium_delete(url)
        if not q:
            raise ShowNotFollowed(f'Show with ID {maze_id} was not followed')

    def get_followed_people(self, embed=None):
        if embed not in [None, 'person']:
            raise InvalidEmbedValue('Value for embed must be "person" or None')
        url = endpoints.followed_people.format('/')
        if embed == 'person':
            url = endpoints.followed_people.format('?embed=person')
        q = self._endpoint_premium_get(url)
        if q:
            return [FollowedPerson(person) for person in q]
        raise NoFollowedPeople('You have not followed any people yet')

    def get_followed_person(self, person_id):
        url = endpoints.followed_people.format('/' + str(person_id))
        q = self._endpoint_premium_get(url)
        if q:
            return FollowedPerson(q)
        raise PersonNotFound(f'Person with ID {person_id} is not followed')

    def follow_person(self, person_id):
        url = endpoints.followed_people.format('/' + str(person_id))
        q = self._endpoint_premium_put(url)
        if not q:
            raise PersonNotFound(f'Person with ID {person_id} does not exist')

    def unfollow_person(self, person_id):
        url = endpoints.followed_people.format('/' + str(person_id))
        q = self._endpoint_premium_delete(url)
        if not q:
            raise PersonNotFollowed(f'Person with ID {person_id} was not followed')

    def get_followed_networks(self, embed=None):
        if embed not in [None, 'network']:
            raise InvalidEmbedValue('Value for embed must be "network" or None')
        url = endpoints.followed_networks.format('/')
        if embed == 'network':
            url = endpoints.followed_networks.format('?embed=network')
        q = self._endpoint_premium_get(url)
        if q:
            return [FollowedNetwork(network) for network in q]
        raise NoFollowedNetworks('You have not followed any networks yet')  # noqa

    def get_followed_network(self, network_id):
        url = endpoints.followed_networks.format('/' + str(network_id))
        q = self._endpoint_premium_get(url)
        if q:
            return FollowedNetwork(q)
        raise NetworkNotFound(f'Network with ID {network_id} is not followed')  # noqa

    def follow_network(self, network_id):
        url = endpoints.followed_networks.format('/' + str(network_id))
        q = self._endpoint_premium_put(url)
        if not q:
            raise NetworkNotFound(f'Network with ID {network_id} does not exist')  # noqa

    def unfollow_network(self, network_id):
        url = endpoints.followed_networks.format('/' + str(network_id))
        q = self._endpoint_premium_delete(url)
        if not q:
            raise NetworkNotFollowed(f'Network with ID {network_id} was not followed')

    def get_followed_web_channels(self, embed=None):
        if embed not in [None, 'webchannel']:
            raise InvalidEmbedValue('Value for embed must be "webchannel" or None')
        url = endpoints.followed_web_channels.format('/')
        if embed == 'webchannel':
            url = endpoints.followed_web_channels.format('?embed=webchannel')
        q = self._endpoint_premium_get(url)
        if q:
            return [FollowedWebChannel(webchannel) for webchannel in q]
        raise NoFollowedWebChannels('You have not followed any Web Channels yet')

    def get_followed_web_channel(self, webchannel_id):
        url = endpoints.followed_web_channels.format('/' + str(webchannel_id))
        q = self._endpoint_premium_get(url)
        if q:
            return FollowedWebChannel(q)
        raise NetworkNotFound(f'Web Channel with ID {webchannel_id} is not followed')  # noqa

    def follow_web_channel(self, webchannel_id):
        url = endpoints.followed_web_channels.format('/' + str(webchannel_id))
        q = self._endpoint_premium_put(url)
        if not q:
            raise WebChannelNotFound(  # noqa
                f'Web Channel with ID {webchannel_id} does not exist')

    def unfollow_web_channel(self, webchannel_id):
        url = endpoints.followed_web_channels.format('/' + str(webchannel_id))
        q = self._endpoint_premium_delete(url)
        if not q:
            raise WebChannelNotFollowed(  # noqa
                f'Web Channel with ID {webchannel_id} was not followed')

    def get_marked_episodes(self, maze_id=None):
        if not maze_id:
            url = endpoints.marked_episodes.format('/')
        else:
            url = endpoints.marked_episodes.format(f'?show_id={maze_id}')
        q = self._endpoint_premium_get(url)
        if q:
            return [MarkedEpisode(episode) for episode in q]
        raise NoMarkedEpisodes('You have not marked any episodes yet')

    def get_marked_episode(self, episode_id):
        url = endpoints.marked_episodes.format(f'/{episode_id}')
        q = self._endpoint_premium_get(url)
        if q:
            return MarkedEpisode(q)
        raise EpisodeNotMarked(f'Episode with ID {episode_id} is not marked')

    def mark_episode(self, episode_id, mark_type):
        types = {'watched': 0, 'acquired': 1, 'skipped': 2}
        try:
            status = types[mark_type]
        except KeyError as exc:
            raise InvalidMarkedEpisodeType(
                'Episode must be marked as "watched", "acquired", or "skipped"') from exc
        payload = {'type': str(status)}
        url = endpoints.marked_episodes.format(f'/{episode_id}')
        q = self._endpoint_premium_put(url, payload=payload)
        if not q:
            raise EpisodeNotFound(f'Episode with ID {episode_id} does not exist')

    def unmark_episode(self, episode_id):
        url = endpoints.marked_episodes.format(f'/{episode_id}')
        q = self._endpoint_premium_delete(url)
        if not q:
            raise EpisodeNotMarked(f'Episode with ID {episode_id} was not marked')

    def get_voted_shows(self, embed=None):
        if embed not in [None, 'show']:
            raise InvalidEmbedValue('Value for embed must be "show" or None')
        url = endpoints.voted_shows.format('/')
        if embed == 'show':
            url = endpoints.voted_shows.format('?embed=show')
        q = self._endpoint_premium_get(url)
        if q:
            return [VotedShow(show) for show in q]
        raise NoVotedShows('You have not voted for any shows yet')

    def get_voted_show(self, maze_id):
        url = endpoints.voted_shows.format('/' + str(maze_id))
        q = self._endpoint_premium_get(url)
        if q:
            return VotedShow(q)
        raise ShowNotVotedFor(f'Show with ID {maze_id} not voted for')

    def remove_show_vote(self, maze_id):
        url = endpoints.voted_shows.format('/' + str(maze_id))
        q = self._endpoint_premium_delete(url)
        if not q:
            raise ShowNotVotedFor(f'Show with ID {maze_id} was not voted for')

    def vote_show(self, maze_id, vote):
        if not 1 <= vote <= 10:
            raise InvalidVoteValue('Vote must be an integer between 1 and 10')
        payload = {'vote': int(vote)}
        url = endpoints.voted_shows.format('/' + str(maze_id))
        q = self._endpoint_premium_put(url, payload=payload)
        if not q:
            raise ShowNotFound(f'Show with ID {maze_id} does not exist')

    def get_voted_episodes(self):
        url = endpoints.voted_episodes.format('/')
        q = self._endpoint_premium_get(url)
        if q:
            return [VotedEpisode(episode) for episode in q]
        raise NoVotedEpisodes('You have not voted for any episodes yet')

    def get_voted_episode(self, episode_id):
        url = endpoints.voted_episodes.format(f'/{episode_id}')
        q = self._endpoint_premium_get(url)
        if q:
            return VotedEpisode(q)
        raise EpisodeNotVotedFor(f'Episode with ID {episode_id} not voted for')

    def remove_episode_vote(self, episode_id):
        url = endpoints.voted_episodes.format(f'/{episode_id}')
        q = self._endpoint_premium_delete(url)
        if not q:
            raise EpisodeNotVotedFor(f'Episode with ID {episode_id} was not voted for')

    def vote_episode(self, episode_id, vote):
        if not 1 <= vote <= 10:
            raise InvalidVoteValue('Vote must be an integer between 1 and 10')
        payload = {'vote': int(vote)}
        url = endpoints.voted_episodes.format(f'/{episode_id}')
        q = self._endpoint_premium_put(url, payload=payload)
        if not q:
            raise EpisodeNotFound(f'Episode with ID {episode_id} does not exist')


# ==================== MODULE-LEVEL FUNCTIONS ====================

def get_show_list(show_name):
    """Return list of Show objects from the TVMaze Show Search endpoint."""
    return show_search(show_name)


def get_people(name):
    """Return list of Person objects from the TVMaze People Search endpoint."""
    people = people_search(name)
    if people:
        return people
    return None


def show_search(show):
    _show = _url_quote(show)
    url = endpoints.show_search.format(_show)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        shows = []
        for result in q:
            show = Show(result['show'])
            show.score = result['score']
            shows.append(show)
        return shows
    raise ShowNotFound(f'Show {show} not found')


def show_single_search(show, embed=None):
    if embed not in [None, 'episodes', 'cast', 'previousepisode', 'nextepisode']:
        raise InvalidEmbedValue(
            'Value for embed must be "episodes", "cast", '
            '"previousepisode", "nextepisode", or None')
    _show = _url_quote(show)
    if embed:
        url = endpoints.show_single_search.format(_show) + '&embed=' + embed
    else:
        url = endpoints.show_single_search.format(_show)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return Show(q)
    raise ShowNotFound(f'show name "{show}" not found')


def lookup_tvrage(tvrage_id):
    url = endpoints.lookup_tvrage.format(tvrage_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return Show(q)
    raise IDNotFound(f'TVRage id {tvrage_id} not found')


def lookup_tvdb(tvdb_id):
    url = endpoints.lookup_tvdb.format(tvdb_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return Show(q)
    raise IDNotFound(f'TVDB ID {tvdb_id} not found')


def lookup_imdb(imdb_id):
    url = endpoints.lookup_imdb.format(imdb_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return Show(q)
    raise IDNotFound(f'IMDB ID {imdb_id} not found')


def get_schedule(country='US', date=str(datetime.today().date())):
    url = endpoints.get_schedule.format(country, date)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return [Episode(episode) for episode in q]
    raise ScheduleNotFound(
        f'Schedule for country {country} at date {date} not found')


def get_full_schedule():
    url = endpoints.get_full_schedule
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return [Episode(episode) for episode in q]
    raise GeneralError('Something went wrong, www.tvmaze.com may be down')


def show_main_info(maze_id, embed=None):
    if embed not in [None, 'episodes', 'cast', 'previousepisode', 'nextepisode']:
        raise InvalidEmbedValue(
            'Value for embed must be "episodes", "cast", '
            '"previousepisode", "nextepisode", or None')
    if embed:
        url = endpoints.show_main_info.format(maze_id) + '?embed=' + embed
    else:
        url = endpoints.show_main_info.format(maze_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return Show(q)
    raise IDNotFound(f'Maze id {maze_id} not found')


def episode_list(maze_id, specials=None):
    if specials:
        url = endpoints.episode_list.format(maze_id) + '&specials=1'
    else:
        url = endpoints.episode_list.format(maze_id)
    q = TVMaze._endpoint_standard_get(url)
    if isinstance(q, list):
        return [Episode(episode) for episode in q]
    raise IDNotFound(f'Maze id {maze_id} not found')


def episode_by_number(maze_id, season_number, episode_number):
    url = endpoints.episode_by_number.format(maze_id, season_number, episode_number)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return Episode(q)
    raise EpisodeNotFound(
        f'Couldn\'t find season {season_number} episode '
        f'{episode_number} for TVMaze ID {maze_id}')


def episodes_by_date(maze_id, airdate):
    try:
        datetime.strptime(airdate, '%Y-%m-%d')
    except ValueError as exc:
        raise IllegalAirDate('Airdate must be string formatted as "YYYY-MM-DD"') from exc
    url = endpoints.episodes_by_date.format(maze_id, airdate)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return [Episode(episode) for episode in q]
    raise NoEpisodesForAirdate(
        f'Couldn\'t find an episode airing {airdate} for TVMaze ID {maze_id}')


def show_cast(maze_id):
    url = endpoints.show_cast.format(maze_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return Cast(q)
    raise CastNotFound(f'Couldn\'t find show cast for TVMaze ID {maze_id}')


def show_index(page=1):
    url = endpoints.show_index.format(page)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return [Show(show) for show in q]
    raise ShowIndexError('Error getting show index, www.tvmaze.com may be down')


def people_search(person):
    person = _url_quote(person)
    url = endpoints.people_search.format(person)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return [Person(person) for person in q]
    raise PersonNotFound(f'Couldn\'t find person {person}')


def person_main_info(person_id, embed=None):
    if embed not in [None, 'castcredits', 'crewcredits']:
        raise InvalidEmbedValue('Value for embed must be "castcredits" or None')
    if embed:
        url = endpoints.person_main_info.format(person_id) + '?embed=' + embed
    else:
        url = endpoints.person_main_info.format(person_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return Person(q)
    raise PersonNotFound(f'Couldn\'t find person {person_id}')


def person_cast_credits(person_id, embed=None):
    if embed not in [None, 'show', 'character']:
        raise InvalidEmbedValue('Value for embed must be "show", "character" or None')
    if embed:
        url = endpoints.person_cast_credits.format(person_id) + '?embed=' + embed
    else:
        url = endpoints.person_cast_credits.format(person_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return [CastCredit(credit) for credit in q]
    raise CreditsNotFound(f'Couldn\'t find cast credits for person ID {person_id}')


def person_crew_credits(person_id, embed=None):
    if embed not in [None, 'show']:
        raise InvalidEmbedValue('Value for embed must be "show" or None')
    if embed:
        url = endpoints.person_crew_credits.format(person_id) + '?embed=' + embed
    else:
        url = endpoints.person_crew_credits.format(person_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return [CrewCredit(credit) for credit in q]
    raise CreditsNotFound(f'Couldn\'t find crew credits for person ID {person_id}')


def get_show_crew(maze_id):
    url = endpoints.show_crew.format(maze_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return [Crew(crew) for crew in q]
    raise CrewNotFound(f'Couldn\'t find crew for TVMaze ID {maze_id}')


def show_updates():
    url = endpoints.show_updates
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return Updates(q)
    raise ShowIndexError('Error getting show updates, www.tvmaze.com may be down')


def show_akas(maze_id):
    url = endpoints.show_akas.format(maze_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return [AKA(aka) for aka in q]
    raise AKASNotFound(f'Couldn\'t find AKA\'s for TVMaze ID {maze_id}')


def show_seasons(maze_id):
    url = endpoints.show_seasons.format(maze_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        season_dict = {}
        for season in q:
            season_dict[season['number']] = Season(season)
        return season_dict
    raise SeasonNotFound(f'Couldn\'t find Season\'s for TVMaze ID {maze_id}')


def season_by_id(season_id):
    url = endpoints.season_by_id.format(season_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return Season(q)
    raise SeasonNotFound(f'Couldn\'t find Season with ID {season_id}')


def episode_by_id(episode_id):
    url = endpoints.episode_by_id.format(episode_id)
    q = TVMaze._endpoint_standard_get(url)
    if q:
        return Episode(q)
    raise EpisodeNotFound(f'Couldn\'t find Episode with ID {episode_id}')
