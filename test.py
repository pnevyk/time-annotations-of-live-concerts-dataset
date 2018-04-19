import unittest
import os
import talc

def mock_get_or_download(destination, item):
    wav_filename = '{}.wav'.format(item['File'])
    wav_fullpath = os.path.join(destination, wav_filename)
    return wav_fullpath

def mock_create_destination_directory(destination):
    pass


talc.talc._get_or_download = mock_get_or_download
talc.talc._create_destination_directory = mock_create_destination_directory


class TALCTest(unittest.TestCase):
    def test_get_metadata(self):
        metadata = talc.get_metadata()
        item = metadata.iloc[0]

        self.assertEqual(len(metadata), 9)
        self.assertEqual(item['Name'], 'AC/DC - Capital Centre 1981')
        self.assertEqual(item['File'], 'acdc-capital-centre-1981')
        self.assertEqual(item['Link'], 'https://www.youtube.com/watch?v=uXVas4bUbsg')
        self.assertEqual(item['Genre'], 'Hard Rock')
        self.assertEqual(item['Audio quality'], 'Bad')

        item = talc.get_metadata('AC/DC - Capital Centre 1981')
        self.assertEqual(item['Name'], 'AC/DC - Capital Centre 1981')
        self.assertEqual(item['File'], 'acdc-capital-centre-1981')
        self.assertEqual(item['Link'], 'https://www.youtube.com/watch?v=uXVas4bUbsg')
        self.assertEqual(item['Genre'], 'Hard Rock')
        self.assertEqual(item['Audio quality'], 'Bad')

    def test_get_audio_list(self):
        audio_list = talc.get_audio_list()
        item = audio_list[0]
        self.assertEqual(len(audio_list), 9)
        self.assertEqual(item[0], 'AC/DC - Capital Centre 1981')
        self.assertTrue(item[1].endswith(os.path.join('.audio', 'acdc-capital-centre-1981.wav')))

        os.environ['TALC_AUDIO_DIRECTORY'] = 'test'
        audio_list = talc.get_audio_list()
        item = audio_list[0]
        self.assertEqual(len(audio_list), 9)
        self.assertEqual(item[0], 'AC/DC - Capital Centre 1981')
        self.assertTrue(item[1].endswith(os.path.join('test', 'acdc-capital-centre-1981.wav')))
        del os.environ['TALC_AUDIO_DIRECTORY']

    def test_get_audio_filepath(self):
        filepath = talc.get_audio_filepath('AC/DC - Capital Centre 1981')
        self.assertTrue(filepath.endswith(os.path.join('.audio', 'acdc-capital-centre-1981.wav')))

        os.environ['TALC_AUDIO_DIRECTORY'] = 'test'
        filepath = talc.get_audio_filepath('AC/DC - Capital Centre 1981')
        self.assertTrue(filepath.endswith(os.path.join('test', 'acdc-capital-centre-1981.wav')))
        del os.environ['TALC_AUDIO_DIRECTORY']

    def test_get_time_annotations(self):
        times = talc.get_time_annotations('AC/DC - Capital Centre 1981')
        self.assertTupleEqual(times[0], (5, 358))
        times = talc.get_time_annotations('AC/DC - Capital Centre 1981', seconds=False)
        self.assertTupleEqual(times[0], ('0:00:05', '0:05:58'))

    def test_stats(self):
        times = talc.get_time_annotations('AC/DC - Capital Centre 1981')
        f_measure, precision, recall, specificity = talc.stats(times, [(0, 3000), (3500, 6318)], 6318)
        stringified = '{:.5f} {:.5f} {:.5f} {:.5f}'.format(f_measure, precision, recall, specificity)
        self.assertEqual(stringified, '0.88699 0.86473 0.91042 0.00631')

    def test_error(self):
        times = talc.get_time_annotations('AC/DC - Capital Centre 1981')
        error = talc.error(times, [(0, 3000), (3500, 6318)], 6318)
        stringified = '{:.5f}'.format(error)
        self.assertEqual(stringified, '0.41992')


if __name__ == '__main__':
    unittest.main()
