
"""
Python  API for the music service.
"""

# Standard library modules

# Installed packages
import requests


class Music():
    """Python API for the music service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the music service. Often
        'http://cmpt756s2:30001/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the music service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, artist, song, orig_artist=None):
        """Create an artist, song pair.

        Parameters
        ----------
        artist: string
            The artist performing song.
        song: string
            The name of the song.
        orig_artist: string or None
            The name of the original performer of this song.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by Music.
            The string is the UUID of this song in the music database.
        """
        payload = {'Artist': artist,
                   'SongTitle': song}
        if orig_artist is not None:
            payload['OrigArtist'] = orig_artist
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['music_id']

    def read(self, m_id):
        """Read an artist, song pair.

        Parameters
        ----------
        m_id: string
            The UUID of this song in the music database.

        Returns
        -------
        status, artist, title, orig_artist

        status: number
            The HTTP status code returned by Music.
        artist: If status is 200, the artist performing the song.
          If status is not 200, None.
        title: If status is 200, the title of the song.
          If status is not 200, None.
        orig_artist: If status is 200 and the song has an
          original artist field, the artist's name.
          If the status is not 200 or there is no original artist
          field, None.
        """
        r = requests.get(
            self._url + m_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None, None

        item = r.json()['Items'][0]
        OrigArtist = (item['OrigArtist'] if 'OrigArtist' in item
                      else None)
        return r.status_code, item['Artist'], item['SongTitle'], OrigArtist

    def delete(self, m_id):
        """Delete an artist, song pair.

        Parameters
        ----------
        m_id: string
            The UUID of this song in the music database.

        Returns
        -------
        Does not return anything. The music delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + m_id,
            headers={'Authorization': self._auth}
        )
