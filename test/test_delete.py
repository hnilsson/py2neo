#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright 2011-2015, Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from py2neo import Node, Rev, Relationship, Path
from py2neo.cypher.delete import DeleteStatement
from py2neo.cypher.error import CypherError
from test.util import Py2neoTestCase


class DeleteTestCase(Py2neoTestCase):
        
    def test_deleting_nothing_does_nothing(self):
        self.graph.delete()
        assert True
        
    def test_can_delete_node(self):
        alice = Node("Person", name="Alice")
        self.graph.create(alice)
        assert alice.exists
        statement = DeleteStatement(self.graph)
        statement.delete(alice)
        assert repr(statement) in [
            "START _0=node({_0})\nDELETE _0",
            "MATCH (_0) WHERE id(_0)={_0}\nDELETE _0",
        ]
        self.graph.delete(alice)
        assert not alice.exists
        
    def test_can_delete_nodes_and_relationship_rel_first(self):
        alice = Node("Person", name="Alice")
        bob = Node("Person", name="Bob")
        ab = Relationship(alice, "KNOWS", bob)
        self.graph.create(alice, bob, ab)
        assert alice.exists
        assert bob.exists
        assert ab.exists
        self.graph.delete(ab, alice, bob)
        assert not alice.exists
        assert not bob.exists
        assert not ab.exists
        
    def test_can_delete_nodes_and_relationship_nodes_first(self):
        alice = Node("Person", name="Alice")
        bob = Node("Person", name="Bob")
        ab = Relationship(alice, "KNOWS", bob)
        self.graph.create(alice, bob, ab)
        assert alice.exists
        assert bob.exists
        assert ab.exists
        self.graph.delete(alice, bob, ab)
        assert not alice.exists
        assert not bob.exists
        assert not ab.exists
        
    def test_cannot_delete_related_node(self):
        alice = Node("Person", name="Alice")
        bob = Node("Person", name="Bob")
        ab = Relationship(alice, "KNOWS", bob)
        self.graph.create(alice, bob, ab)
        assert alice.exists
        assert bob.exists
        assert ab.exists
        with self.assertRaises(CypherError):
            self.graph.delete(alice)
        self.graph.delete(alice, bob, ab)
        
    def test_can_delete_path(self):
        path = Path({}, "LOVES", {}, Rev("HATES"), {}, "KNOWS", {})
        self.graph.create(path)
        assert path.exists
        self.graph.delete(path)
        assert not path.exists
        
    def test_cannot_delete_other_types(self):
        with self.assertRaises(TypeError):
            self.graph.delete("not a node or a relationship")
