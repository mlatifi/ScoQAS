__author__ = 'majid'



""" A Python Class
A simple Python graph class, demonstrating the essential
facts and functionalities of graphs.
"""


class Graph(object):

    def __init__(self, graph_sent={},graph_inst={}):
        """ initializes a graph object """
        self.__graph_sent = graph_sent
        self.__graph_inst = graph_inst

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_sent.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self.__graph_sent, a key "vertex" with an empty
            list as a value is added to the ontology.
            Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_sent:
            self.__graph_sent[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        print "Order of vertex1---vertex2:",vertex1,vertex2
        if vertex1 in self.__graph_sent:
            self.__graph_sent[vertex1].append(vertex2)
        else:
            self.__graph_sent[vertex1] = [vertex2]

    def add_edge_instance_of(self, slot,instance):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        # edge = set(edge)
        # (vertex1, vertex2) = tuple(edge)
        instTmp="Instance Of"
        slot_instance={slot,instance}
        edge=set(slot_instance)
        (vertex1,vertex2)=tuple(edge)
        print "Order of vertex1---vertex2:",vertex1,vertex2
        if vertex1 in self.__graph_sent:
            print "VERTEX_1 IS   in graphsent",vertex1,vertex2
            if vertex2 in self.__graph_inst:
                print "INSTance  IS   in graph_instt",instTmp
                self.__graph_inst[slot,instance].append(vertex2)
            else:
                print "INSTance  IS NOTTT!!  in graph_instt",vertex2
                self.__graph_inst[slot,instance]=[]
                self.__graph_inst[slot,instance].append(vertex2)
                print "OKKK",self.__graph_inst[slot,instance]

        else:
            print "VERTEX_1 IS NOTTT !!! in graphsent",vertex1
            self.__graph_sent[vertex1] = []
            if vertex2 in self.__graph_inst:
                print "INSTance  IS   in graph_instt",instTmp
                self.__graph_inst[slot,instance].append(vertex2)
            else:
                self.__graph_inst[slot,instance]=[vertex2]


    def __generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for vertex in self.__graph_sent:
            for neighbour in self.__graph_sent[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "Nodes:\n"
        for k in self.__graph_sent:
            res += str(k) + " "
        res += "\nInstance Slot: "
        for inst in self.__graph_inst:
            res += str(inst) + " "
        res += "\nEdges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "

        return res





def find_isolated_nodes(graph):
    """ returns a list of isolated nodes. """
    isolated = []
    for node in graph:
        if not graph[node]:
            isolated += node
    return isolated



def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))

    return edges







def creatGraphSentence(s,WorkingDirectory):
    default_graph_uri = WorkingDirectory + 'rdfstore/'
        # "http://rdflib.net/rdfstore"
    configString = "/var/tmp/rdfstore"
    # store = plugin.get('question22', Store)('rdfstore')

    # Open previously created store, or create it if it doesn't exist yet
    graph = rdflib.Graph('Sleepycat')
    # path = mkdtemp()
    print "path:", default_graph_uri
    rt = graph.open(default_graph_uri, create=True)
    # if rt == NO_STORE:
    #     # There is no underlying SentenceGraph infrastructure, create it
    #     graph.open(default_graph_uri, create=True)
    # else:
    #     assert rt == VALID_STORE, "The underlying store is corrupt"
    #
    print "Triples in graph before add: %s", len(graph),rt

    myrdflib = Namespace(WorkingDirectory + 'test/')
    graph.bind("test.rdf", WorkingDirectory + "test/")


    graph.add((myrdflib['pic:1'], myrdflib['name'], Literal('Jane & Bob')))
    graph.add((myrdflib['pic:2'], myrdflib['name'], Literal('Squirrel in Tree')))
    graph.commit()
    print "Triples in graph after add: ", len(graph)
    # display the graph in RDF/XML
    # print graph.serialize()
    graph.close()


    bob = URIRef("http://example.com/people/Bob")
    anode = BNode()
    n = Namespace("http://example.org/people/")
    my_data = '''
    <rdf:RDF
       xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'
       xmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'
    >
      <rdf:Description>
        <rdfs:label>Example</rdfs:label>
        <rdfs:comment>This is really just an example.</rdfs:comment>
      </rdf:Description>
    </rdf:RDF>
    '''

    fd, file_name = tempfile.mkstemp("Question22.rdf")
    f = os.fdopen(fd, 'w')
    dummy = f.write(my_data)
    print "fd,filem name,f",fd,file_name,dummy,f
    f.close()

def addTriples():
    g=rdflib.Graph()
    statementId = BNode()
    g.add((statementId, RDF.type, RDF.Statement))
    g.add((statementId, RDF.subject,
           URIRef(u'http://rdflib.net/store/ConjunctiveGraph')))
    g.add((statementId, RDF.predicate, RDFS.label))
    g.add((statementId, RDF.object, Literal("Conjunctive Graph")))
    print(len(g))
    for s, p, o in g:
        print(type(s))

