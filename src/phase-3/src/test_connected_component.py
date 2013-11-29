import psycopg2
import unittest
from cc.cc import *
from common.util import *

class ConnectedComponentTest(unittest.TestCase):
	def setUp(self):
		self.conn = psycopg2.connect(database="mydb", host="127.0.0.1")

	def tearDown(self):
		pass

	#@unittest.skip("")
	def test_trec_wt10(self):
		"""http://konect.uni-koblenz.de/networks/trec-wt10g"""
		data_file = "../data/trec_wt10.txt"
		edge_table = "trec_wt10"
		target_table = "cc_trec_wt10"
		load_weighted_graph(edge_table, data_file, False, self.conn, ' ')
		print "trec_wt10.."
		compute_cc(self.conn, edge_table, target_table)

	@unittest.skip("")
	def test_youtube(self):
		"""http://snap.stanford.edu/data/com-Youtube.html"""
		data_file = "../data/youtube.txt"
		edge_table = "youtube"
		target_table = "cc_youtube"
		load_unweighted_graph(edge_table, data_file, False, self.conn)
		print "youtube.."
		compute_cc(self.conn, edge_table, target_table)

	@unittest.skip("")
	def test_pokec(self):
		""""http://snap.stanford.edu/data/soc-pokec.html"""
		data_file = "../data/pokec.txt"
		edge_table = "pokec"
		target_table = "cc_pokec"
		load_unweighted_graph(edge_table, data_file, False, self.conn)
		print "pokec.."
		compute_cc(self.conn, edge_table, target_table)

	@unittest.skip("")
	def test_web_google(self):
		"""http://snap.stanford.edu/data/web-Google.html"""
		data_file = "../data/web_google.txt"
		edge_table = "web_google"
		target_table = "cc_web_google"
		load_unweighted_graph(edge_table, data_file, False, self.conn)
		print "web google.."
		compute_cc(self.conn, edge_table, target_table)

	@unittest.skip("")
	def test_amazon(self):
		"""http://snap.stanford.edu/data/com-Amazon.html"""
		data_file = "../data/amazon.txt"
		edge_table = "amazon"
		target_table = "cc_amazon"
		load_unweighted_graph(edge_table, data_file, False, self.conn)
		print "amazon.."
		compute_cc(self.conn, edge_table, target_table)

	@unittest.skip("")
	def test_email_EuAll(self):
		"""http://snap.stanford.edu/data/email-EuAll.html"""
		data_file = "../data/email-EuAll.txt"
		edge_table = "email_EuAll"
		target_table = "cc_email_EuAll"
		load_unweighted_graph(edge_table, data_file, False, self.conn)
		print "email_EuAll.."
		compute_cc(self.conn, edge_table, target_table)


	@unittest.skip("")
	def test_wiki_talk(self):
		"""http://snap.stanford.edu/data/wiki-Talk.html"""
		data_file = "../data/wiki-talk.txt"
		edge_table = "wiki_talk"
		target_table = "cc_wiki_talk"
		load_unweighted_graph(edge_table, data_file, False, self.conn)
		print "wiki_talk.."
		compute_cc(self.conn, edge_table, target_table)


	@unittest.skip("")
	def test_soc_sign_epinions(self):
		"""http://snap.stanford.edu/data/soc-sign-epinions.html"""
		data_file = "../data/soc-sign-epinions.txt"
		edge_table = "soc_sign_epinions"
		target_table = "cc_soc_sign_epinions"
		load_weighted_graph(edge_table, data_file, False, self.conn)
		print "soc_sign_epinions.."
		compute_cc(self.conn, edge_table, target_table)