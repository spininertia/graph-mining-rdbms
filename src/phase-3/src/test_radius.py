import psycopg2
import unittest
from radius.radius import *
from common.util import *

class RadiusTest(unittest.TestCase):
	def setUp(self):
		self.conn = psycopg2.connect(database="mydb", host="127.0.0.1")

	def tearDown(self):
		pass

	@unittest.skip("")
	def test_amazon(self):
		"""http://snap.stanford.edu/data/com-Amazon.html"""
		data_file = "../data/amazon.txt"
		edge_table = "amazon"
		dataset = "cc_amazon"
		load_unweighted_graph(edge_table, data_file, False, self.conn)
		print "amazon.."
		compute_radius(self.conn, edge_table, dataset, 4)

	@unittest.skip("")
	def test_soc_sign_epinions(self):
		"""http://snap.stanford.edu/data/soc-sign-epinions.html"""
		data_file = "../data/soc-sign-epinions.txt"
		edge_table = "soc_sign_epinions"
		dataset = "soc_sign_epinions"
		load_weighted_graph(edge_table, data_file, False, self.conn)
		print "soc_sign_epinions.."
		compute_radius(self.conn, edge_table, dataset, 8)

	#@unittest.skip("")
	def test_email_EuAll(self):
		"""http://snap.stanford.edu/data/email-EuAll.html"""
		data_file = "../data/email-EuAll.txt"
		edge_table = "email_EuAll"
		dataset = "email_EuAll"
		load_unweighted_graph(edge_table, data_file, False, self.conn)
		print "email_EuAll.."
		compute_radius(self.conn, edge_table, dataset, 8)

	@unittest.skip("")
	def test_web_google(self):
		"""http://snap.stanford.edu/data/web-Google.html"""
		data_file = "../data/web_google.txt"
		edge_table = "web_google"
		dataset = "web_google"
		load_unweighted_graph(edge_table, data_file, False, self.conn)
		print "web google.."
		compute_radius(self.conn, edge_table, dataset, 1)

	@unittest.skip("")
	def test_youtube(self):
		"""http://snap.stanford.edu/data/com-Youtube.html"""
		data_file = "../data/youtube.txt"
		edge_table = "youtube"
		dataset = "youtube"
		load_unweighted_graph(edge_table, data_file, False, self.conn)
		print "youtube.."
		compute_radius(self.conn, edge_table, dataset, 1)
