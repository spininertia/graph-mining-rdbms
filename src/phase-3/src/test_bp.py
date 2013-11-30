import psycopg2
import unittest
from bp.bp import *
from common.util import *

class BeliefPropagationTest(unittest.TestCase):
	def setUp(self):
		self.conn = psycopg2.connect(database="mydb", host="127.0.0.1")

	def tearDown(self):
		pass

	#@unittest.skip("")
	def test_amazon(self):
		"""http://snap.stanford.edu/data/com-Amazon.html"""
		data_file = "../data/amazon.txt"
		edge_table = "amazon"
		dataset = "amazon"
		load_unweighted_graph(edge_table, data_file, True, self.conn)
		print "amazon.."
		compute_bp(self.conn, edge_table, dataset)

	#@unittest.skip("")
	def test_soc_sign_epinions(self):
		"""http://snap.stanford.edu/data/soc-sign-epinions.html"""
		data_file = "../data/soc-sign-epinions.txt"
		edge_table = "soc_sign_epinions"
		dataset = "soc_sign_epinions"
		load_weighted_graph(edge_table, data_file, True, self.conn)
		print "soc_sign_epinions.."
		compute_bp(self.conn, edge_table, dataset)

	#@unittest.skip("")
	def test_email_EuAll(self):
		"""http://snap.stanford.edu/data/email-EuAll.html"""
		data_file = "../data/email-EuAll.txt"
		edge_table = "email_EuAll"
		dataset = "email_EuAll"
		load_unweighted_graph(edge_table, data_file, True, self.conn)
		print "email_EuAll.."
		compute_bp(self.conn, edge_table, dataset)


	#@unittest.skip("")
	def test_web_google(self):
		"""http://snap.stanford.edu/data/web-Google.html"""
		data_file = "../data/web_google.txt"
		edge_table = "web_google"
		dataset = "web_google"
		load_unweighted_graph(edge_table, data_file, True, self.conn)
		print "web google.."
		compute_bp(self.conn, edge_table, dataset)

	#@unittest.skip("")
	def test_youtube(self):
		"""http://snap.stanford.edu/data/com-Youtube.html"""
		data_file = "../data/youtube.txt"
		edge_table = "youtube"
		dataset = "youtube"
		load_unweighted_graph(edge_table, data_file, True, self.conn)
		print "youtube.."
		compute_bp(self.conn, edge_table, dataset)

	#@unittest.skip("")
	def test_dblp(self):
		"""dblp"""
		data_file = "../data/dblp.txt"
		edge_table = "dblp"
		dataset = "dblp"
		load_unweighted_graph(edge_table, data_file, True, self.conn)
		print "dblp.."
		compute_bp(self.conn, edge_table, dataset)

	@unittest.skip("")
	def test_synthetic(self):
		"""test_synthetic"""
		data_file = "../data/synthetic_bp.txt"
		edge_table = "synthetic"
		dataset = "synthetic"
		load_weighted_graph(edge_table, data_file, False, self.conn, " ")
		print "synthetic.."
		compute_bp(self.conn, edge_table, dataset, True)

	@unittest.skip("")
	def test_advogato(self):
		"""test_advogato"""
		data_file = "../data/advogato.txt"
		edge_table = "advogato"
		dataset = "advogato"
		load_weighted_graph(edge_table, data_file, True, self.conn, " ")
		print "advogato.."
		compute_bp(self.conn, edge_table, dataset, True)

