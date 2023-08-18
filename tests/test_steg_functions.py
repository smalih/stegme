import unittest, sys, os
from PIL import Image

sys.path.append('..')

from steg import *

class TestSteg(unittest.TestCase):
    def setUp(self):
        folder = './output_images'
        for filename in os.listdir(folder): # empty output folder at start of each time tests executed
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        self.message = "seo london"
    

    def test_valid_encode_png_with_dest(self):
        self.assertEqual(encode('input_images/input1.png', 'image/png', self.message, 'output_images/output1.png'), None)
        self.assertTrue(os.path.isfile('./output_images/output1.png'))

    def test_valid_encode_jpeg_with_dest(self):
        self.assertEqual(encode('input_images/input2.jpg', 'image/jpeg', self.message, 'output_images/output2.png'), None)
        self.assertTrue(os.path.isfile('./output_images/output2.png'))

    def test_valid_encode_gif_with_dest(self):
        self.assertEqual(encode('input_images/input3.gif', 'image/gif', self.message, 'output_images/output3.gif'), None)
        self.assertTrue(os.path.isfile('./output_images/output3.gif'))

    def test_valid_encode_png_with_no_dest(self):
        self.assertNotIsInstance(encode('input_images/input1.png', 'image/png', self.message), type(None))
    
    def test_valid_encode_jpeg_with_no_dest(self):
        self.assertNotIsInstance(encode('input_images/input2.jpg', 'image/jpeg', self.message), type(None)) 
    
    def test_valid_encode_gif_with_no_dest(self):
        self.assertNotIsInstance(encode('input_images/input3.gif', 'image/gif', self.message), type(None)) 

    def test_valid_decode_png(self):
        self.assertEqual(decode('./test_output_images/output1.png', 'image/png'), self.message)

    def test_valid_decode_from_jpeg(self):
        self.assertEqual(decode('./test_output_images/output2.png', 'image/jpeg'), self.message)

    def test_valid_decode_from_gif(self):
        self.assertEqual(decode('./test_output_images/output3.gif', 'image/gif'), self.message)




if __name__ == '__main__':
    unittest.main()