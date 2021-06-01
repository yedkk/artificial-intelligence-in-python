############################################################
# CMPSC 442: Homework 4
############################################################

student_name = "Kangdong Yuan"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import itertools

############################################################
# Section 1: Propositional Logic
############################################################


class Expr(object):

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

class Atom(Expr):
    def __init__(self, name):
        self.name = name
        self.hashable = name

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

    def __eq__(self, other):
        if type(self) == type(other):
            if self.name == other.name:
                return True
        return False

    def __repr__(self):
        return "Atom({})".format(self.name)

    def atom_names(self):
        return set([self.name])

    def evaluate(self, assignment):
        return assignment[self.name]

    def to_cnf(self):
        if type(self.name) == bool:
            return self.name
        return self


class Not(Expr):
    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

    def __eq__(self, other):
        if type(self) == type(other):
            if self.arg == other.arg:
                return True
        return False

    def __repr__(self):
        return "Not({})".format(self.arg)

    def atom_names(self):
        return self.arg.atom_names()

    def evaluate(self, assignment):
        return not self.arg.evaluate(assignment)

    def to_cnf(self):
        if type(self.arg) == Atom:
            return self
        if type(self.arg) == Implies:
            return And(self.arg.left, Not(self.arg.right)).to_cnf()
        if type(self.arg) == And:
            return Or(*map(Not, self.arg.conjuncts)).to_cnf()
        if type(self.arg) == Not:
            return self.arg.arg.to_cnf()
        if type(self.arg) == Iff:
            right, left = self.arg.right, self.arg.left
            return Or(Not(Implies(left, right)), Not(Implies(right, left))).to_cnf()
        if type(self.arg) == Or:
            return And(*map(Not, self.arg.disjuncts)).to_cnf()


class And(Expr):
    def __init__(self, *conjuncts):
        self.conjuncts = frozenset(conjuncts)
        self.hashable = self.conjuncts

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

    def __eq__(self, other):
        if type(self) == type(other):
            if self.conjuncts == other.conjuncts:
                return True
        return False

    def __repr__(self):
        temp = ", ".join([repr(x) for x in self.conjuncts])
        return "And({})".format(temp)

    def atom_names(self):
        name = set([])
        for i in self.conjuncts:
            name = name.union(i.atom_names())
        return name

    def evaluate(self, assignment):
        result = True
        for parts in self.conjuncts:
            result = result and parts.evaluate(assignment)
        return result

    def cnfhelper(self, store):
        cnf = []
        for j in store:
            if isinstance(j, And):
                for k in j.hashable:
                    cnf.append(k)
            else:
                cnf.append(j)
        return cnf

    def to_cnf(self):
        store = []
        for i in self.hashable:
            store.append(i.to_cnf())
        cnf = self.cnfhelper(store)
        return And(*cnf)


class Or(Expr):
    def __init__(self, *disjuncts):
        self.disjuncts = frozenset(disjuncts)
        self.hashable = self.disjuncts

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

    def __eq__(self, other):
        if type(self) == type(other):
            if self.disjuncts == other.disjuncts:
                return True
        return False

    def __repr__(self):
        temp = ", ".join([repr(x) for x in self.disjuncts])
        return "Or({})".format(temp)

    def atom_names(self):
        name = set([])
        for i in self.disjuncts:
            name = name.union(i.atom_names())
        return name

    def evaluate(self, assignment):
        result = False
        for d in self.disjuncts:
            result = result or d.evaluate(assignment)
        return result

    def cnf_helper(self,or_store, atom_store):
        combine_list = []
        for i in range(len(or_store)):
            if isinstance(or_store[i], Atom) or isinstance(or_store[i], Not):
                atom_store.append(or_store[i])
            elif isinstance(or_store[i], Or):
                atom_store = atom_store + list(or_store[i].disjuncts)
            else:
                combine_list.append(or_store[i].conjuncts)
        return combine_list

    def cnf_append(self):
        or_store = []
        for i in self.disjuncts:
            if isinstance(i, Or):
                for j in i.disjuncts:
                    or_store.append(j.to_cnf())
            else:
                or_store.append(i.to_cnf())
        return or_store

    def cnf_final(self, iter_combine, atom_store):
        final = []
        for i in range(len(iter_combine)):
            list_i = list(iter_combine[i])
            iter_combine[i] = list_i + atom_store
            for j in iter_combine[i]:
                if isinstance(j, Or):
                    for x in j.disjuncts:
                        iter_combine[i].append(x)
                    iter_combine[i].remove(j)
            not_temp = {Not(x).to_cnf() for x in iter_combine[i]}
            if len(not_temp.intersection(set(iter_combine[i]))) == 0:
                final.append(Or(*iter_combine[i]))
        return final

    def to_cnf(self):
        atom_store,  combine_list = [], []
        or_store = self.cnf_append()
        for i in range(len(or_store)):
            if isinstance(or_store[i], Atom) or isinstance(or_store[i], Not):
                atom_store.append(or_store[i])
            elif isinstance(or_store[i], Or):
                atom_store = atom_store + list(or_store[i].disjuncts)
            else:
                combine_list.append(or_store[i].conjuncts)
        iter_combine = list(itertools.product(*combine_list))
        if len(combine_list) == 0:
            return Or(*atom_store)
        else:
            final = self.cnf_final(iter_combine, atom_store)
            return And(*final)


class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

    def __eq__(self, other):
        condition1 = type(self) == type(other)
        condition2 = self.left == other.left
        condition3 = self.right == other.right
        condition4 = condition1 and condition2 and condition3
        return condition4

    def __repr__(self):
        return "Or({}, {})".format(self.left, self.right)

    def atom_names(self):
        name = self.left.atom_names()
        return name.union(self.right.atom_names())

    def evaluate(self, assignment):
        table = {(True, True): True, (True, False): False, (False, True): True, (False, False): True}
        return table[(self.left.evaluate(assignment), self.right.evaluate(assignment))]

    def to_cnf(self):
        return Or(Not(self.left), self.right).to_cnf()


class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

    def __eq__(self, other):
        if type(self) == type(other):
            if self.left == other.right and self.right == other.left:
                return True
            elif self.left == other.left and self.right == other.right:
                return True
        return False

    def __repr__(self):
        return "Iff({}, {})".format(self.left, self.right)

    def atom_names(self):
        name = self.left.atom_names()
        return name.union(self.right.atom_names())

    def evaluate(self, assignment):
        table = {(True, True): True, (True, False): False, (False, True): False, (False, False): True}
        return table[(self.left.evaluate(assignment), self.right.evaluate(assignment))]

    def to_cnf(self):
        return And(Or(Not(self.left), self.right), Or(Not(self.right), self.left)).to_cnf()


def satisfying_assignments(expr):
    names = list(expr.atom_names())
    all = list(itertools.product([False, True], repeat=len(names)))
    for assign in all:
        assignment = {names[i]: assign[i] for i in range(len(names))}
        if expr.evaluate(assignment):
            yield assignment


class KnowledgeBase(object):
    def __init__(self):
        self.facts = set([])

    def get_facts(self):
        return self.facts

    def tell(self, expr):
        self.facts.add(expr.to_cnf())

    def ask_assumption(self,expr):
        return And(*self.get_facts(), Not(expr)).to_cnf()

    def ask(self, expr):
        try:
            next(satisfying_assignments(self.ask_assumption(expr)))
        except:
            return True
        return False


############################################################
# Section 2: Logic Puzzles
############################################################

# Puzzle 1

kb1 = KnowledgeBase()

m1 = Atom("mythical")
m2 = Atom("mortal")
m3 = Atom("mammal")
h1 = Atom("horned")
m4 = Atom("magical")

kb1.tell(Implies(m1, Not(m2)))
kb1.tell(Implies(Not(m1), And(m2, m3)))
kb1.tell(Implies(Or(Not(m2), m3), h1))
kb1.tell(Implies(h1, m4))

# Write an Expr for each query that should be asked of the knowledge base

mythical_query = m1
magical_query = m4
horned_query = h1


# Record your answers as True or False; if you wish to use the above queries,
# they should not be run when this file is loaded

is_mythical = False
is_magical = True
is_horned = True



# Puzzle 2

# Write an Expr of the form And(...) encoding the constraints
party_constraints = And(Implies(Or(Atom("m"), Atom("a")), Atom("j")), Implies(Not(Atom("m")), Atom("a")),
                        Implies(Atom("a"), Not(Atom("j"))))

# Compute a list of the valid attendance scenarios using a call to
# satisfying_assignments(expr)
valid_scenarios = [{'j': True, 'm': True, 'a': False}]

# Write your answer to the question in the assignment
puzzle_2_question = """
There is only one way that the guests can attend without violating the constraints, 
where John and Mary will come and Ann will not come. Since if Ann comes, then John will not come, 
so Ann and John will not both come. And if Mary does not come, Ann will come, so we can say that if Mary does not come, 
John will not come, and Mary and John will come if either Ann or Mary come. 
Therefore, we know that John and Mary will come and Ann will not come.
"""

# Puzzle 3

# Populate the knowledge base using statements of the form kb3.tell(...)
kb3 = KnowledgeBase()

prize_room_1 = Atom("p1")
prize_room_2 = Atom("p2")
empty_room_1 = Atom("e1")
empty_room_2 = Atom("e2")
sign_1_true = Atom("s1")
sign_2_true = Atom("s2")

kb3.tell(Iff(prize_room_1, Not(empty_room_1)))
kb3.tell(Iff(prize_room_2, Not(empty_room_2)))
kb3.tell(Iff(And(prize_room_1, empty_room_2), sign_1_true))
kb3.tell(Iff(Or(And(prize_room_1, empty_room_2), And(empty_room_1, prize_room_2)), sign_2_true))
kb3.tell(And(Or(sign_1_true, sign_2_true), Or(Not(sign_1_true), Not(sign_2_true))))


# Write your answer to the question in the assignment; the queries you make
# should not be run when this file is loaded
puzzle_3_question = """
We know that the first room is empty and the second room contains a prize. 
We know that the sign on the second door is true, because only one sign can be true, 
if the sign on the first door is true, then the sign on the second door must be true. 
Therefore, the sign on the first door is false, and the sign on the second door is true. 
Since the sign on the first door is false, then we know that the first room is empty and the second room contains a prize.
"""

# Puzzle 4

# Populate the knowledge base using statements of the form kb4.tell(...)
kb4 = KnowledgeBase()

adams_query = And(Atom("ia"), Atom("kb"), Not(Atom("kc")))
brown_query = And(Atom("ib"), Not(Atom("kb")))
clark_query = And(Atom("ic"), Or(Not(Atom("ia")), Not(Atom("ib"))), And(Atom("ka"), Atom("kb")))
kb4.tell(Or(And(adams_query, brown_query, Not(clark_query)), And(adams_query, Not(brown_query), clark_query),
            And(Not(adams_query), brown_query, clark_query)))

# innocent_query = Or(And(Atom("ia"), Atom("ib"), Not(Atom("ic"))), And(Atom("ia"), Not(Atom("ib")), Atom("ic")),
#                     And(Not(Atom("ia")), Atom("ib"), Atom("ic")))

# Uncomment the line corresponding to the guilty suspect
# guilty_suspect = "Adams"
guilty_suspect = "Brown"
# guilty_suspect = "Clark"
# Describe the queries you made to ascertain your findings
puzzle_4_question = """
Since the two innocent men are telling the truth, and both Adams and Clark say that Brown knows the victim. 
Therefore, they must be telling the truth and Brown is not. So Brown is guilty.
"""
a, b, c = map(Atom, "abc")
print(Iff(a, Or(b, c)).to_cnf())
