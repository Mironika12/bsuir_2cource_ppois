#include "D:\\ppois\\ppois_1\\treenode.h"
#include "D:\\ppois\\ppois_1\\dict.h"
#include <UnitTest++.h>
#include <string>
#include <sstream>
#include <windows.h>

using namespace std;

// ============================================================================
//                          ТЕСТЫ ДЛЯ TreeNode
// ============================================================================
SUITE(TreeNodeTests)
{
    TEST(Constructor_SetsPairCorrectly)
    {
        pair<string, string> p("word", "translation");
        TreeNode node(p);
        CHECK_EQUAL("word", node.getWords().first);
        CHECK_EQUAL("translation", node.getWords().second);
        CHECK(node.getLeft() == nullptr);
        CHECK(node.getRight() == nullptr);
    }

    TEST(SetLeft_SetsCorrectly)
    {
        TreeNode parent(make_pair("root", "корень"));
        TreeNode* leftChild = new TreeNode(make_pair("left", "левый"));
        parent.setLeft(leftChild);
        CHECK_EQUAL(leftChild, parent.getLeft());
    }

    TEST(SetRight_SetsCorrectly)
    {
        TreeNode parent(make_pair("root", "корень"));
        TreeNode* rightChild = new TreeNode(make_pair("right", "правый"));
        parent.setRight(rightChild);
        CHECK_EQUAL(rightChild, parent.getRight());
    }

    TEST(GetPair_ReturnsCorrectValue)
    {
        pair<string, string> p("word", "translation");
        TreeNode node(p);
        auto result = node.getWords();
        CHECK_EQUAL(p.first, result.first);
        CHECK_EQUAL(p.second, result.second);
    }

    TEST(SetPair_UpdatesValue)
    {
        TreeNode node(make_pair("a", "b"));
        pair<string, string> newPair("c", "d");
        node.setWords(newPair);
        CHECK_EQUAL("c", node.getWords().first);
        CHECK_EQUAL("d", node.getWords().second);
    }

    TEST(GetLeftAndRightInitiallyNull)
    {
        TreeNode node(make_pair("x", "y"));
        CHECK(node.getLeft() == nullptr);
        CHECK(node.getRight() == nullptr);
    }

    TEST(MultipleAssignmentsLeftRight)
    {
        TreeNode root(make_pair("root", "корень"));
        TreeNode* left = new TreeNode(make_pair("left", "левый"));
        TreeNode* right = new TreeNode(make_pair("right", "правый"));
        TreeNode* right2 = new TreeNode(make_pair("right2", "правый2"));

        root.setLeft(left);
        root.setRight(right);
        CHECK_EQUAL(left, root.getLeft());
        CHECK_EQUAL(right, root.getRight());

        root.setRight(right2);
        CHECK_EQUAL(right2, root.getRight());
    }

    TEST(SetPairThenGetPair)
    {
        TreeNode node(make_pair("old", "старый"));
        pair<string, string> updated("new", "новый");
        node.setWords(updated);
        CHECK_EQUAL("new", node.getWords().first);
        CHECK_EQUAL("новый", node.getWords().second);
    }

    TEST(MutateThroughPointer)
    {
        TreeNode node(make_pair("key", "значение"));
        TreeNode* ptr = &node;
        CHECK_EQUAL("key", ptr->getWords().first);
        CHECK_EQUAL("значение", ptr->getWords().second);

        pair<string, string> newPair("ключ", "value");
        ptr->setWords(newPair);
        CHECK_EQUAL("ключ", ptr->getWords().first);
        CHECK_EQUAL("value", ptr->getWords().second);
    }

    TEST(InsertAndFind_SingleNode)
    {
        TreeNode root({ "m", "1" });
        TreeNode* found = root.find("m");
        CHECK(found != nullptr);
        CHECK_EQUAL("1", found->getWords().second);
        CHECK(root.find("x") == nullptr);
    }

    TEST(Insert_MultipleNodes)
    {
        TreeNode root({ "m", "1" });
        root.insert({ "a", "2" });
        root.insert({ "z", "3" });
        CHECK_EQUAL("2", root.find("a")->getWords().second);
        CHECK_EQUAL("1", root.find("m")->getWords().second);
        CHECK_EQUAL("3", root.find("z")->getWords().second);
    }

    TEST(Find_NotFound)
    {
        TreeNode root({ "m", "1" });
        root.insert({ "a", "2" });
        CHECK(root.find("zzz") == nullptr);
    }

    TEST(Remove_Leaf)
    {
        TreeNode* root = new TreeNode({ "m", "1" });
        root->insert({ "a", "2" });
        TreeNode* newroot = root->remove({ "a", "" });

        CHECK_EQUAL(root, newroot);
        CHECK(root->find("a") == nullptr);
        CHECK_EQUAL("1", root->find("m")->getWords().second);

        delete root;
    }

    TEST(Remove_NodeWithOneChild)
    {
        TreeNode* root = new TreeNode({ "m", "1" });
        root->insert({ "a", "2" });
        root->insert({ "b", "3" });

        /*
            m
           /
          a
           \
            b
        */

        TreeNode* newroot = root->remove({ "a", "" });

        CHECK_EQUAL(root, newroot);
        CHECK(root->find("a") == nullptr);
        CHECK_EQUAL("3", root->find("b")->getWords().second);

        delete root;
    }

    TEST(Remove_NodeWithTwoChildren)
    {
        TreeNode* root = new TreeNode({ "m", "1" });

        root->insert({ "a", "2" });
        root->insert({ "z", "3" });
        root->insert({ "b", "4" });
        root->insert({ "y", "5" });

        /*
                 m
               /   \
              a     z
               \   /
                b y
        */

        TreeNode* newroot = root->remove({ "m", "" });

        CHECK(newroot->find("m") == nullptr);
        CHECK(newroot->find("a") != nullptr);
        CHECK(newroot->find("b") != nullptr);
        CHECK(newroot->find("z") != nullptr);
        CHECK(newroot->find("y") != nullptr);

        if (newroot) delete newroot;
    }

    TEST(Remove_RootSingleNode)
    {
        TreeNode* root = new TreeNode({ "m", "1" });
        TreeNode* newroot = root->remove({ "m", "" });

        CHECK(newroot == nullptr);
    }

    TEST(NodeCount)
    {
        TreeNode* root = new TreeNode(make_pair("cat", "кот"));
        root = root->insert(make_pair("dog", "собака"));
        root = root->insert(make_pair("root", "корень"));
        root = root->insert(make_pair("sun", "солнце"));

        CHECK_EQUAL(4, root->nodeCount());

        root = root->remove(make_pair("sun", "солнце"));
        CHECK_EQUAL(3, root->nodeCount());
        delete root;
    }

    TEST(EqualAndNotEqualOps)
    {
        TreeNode node1(make_pair("cat", "кот"));
        TreeNode node2(make_pair("cat", "кот"));
        TreeNode node3(make_pair("dog", "собака"));
        CHECK(node1 == node2);
        CHECK(node1 != node3);
    }

    TEST(GetAdressRuWord)
    {
        TreeNode node(make_pair("cat", "кот"));
        const string& res = node.getRuAdress();
        CHECK_EQUAL(res, node.getWords().second);
    }
}

// ============================================================================
//                          ТЕСТЫ ДЛЯ Dict
// ============================================================================
SUITE(DictTests)
{
    TEST(Constructor_Empty)
    {
        Dict d;
        CHECK(d.empty());
        CHECK(d.getRoot() == nullptr);
        d += make_pair<string, string>("cat", "кот");
        CHECK(d.getRoot() != nullptr);
    }

    TEST(Constructor_WithPair)
    {
        Dict d({ "apple", "яблоко" });
        CHECK(!d.empty());
        CHECK_EQUAL("яблоко", d["apple"]);
    }

    TEST(Destructor)
    {
        Dict* d = new Dict({ "apple", "яблоко" });
        CHECK(!((*d).empty()));
        delete d;
    }

    TEST(OperatorPlusEquals_AddWord)
    {
        Dict d;
        d += { "cat", "кот" };
        CHECK_EQUAL("кот", d["cat"]);
    }

    TEST(OperatorPlusEquals_DuplicateKey)
    {
        Dict d;
        d += { "apple", "яблоко" };
        d += { "apple", "мяблоко" };
        CHECK_EQUAL("яблоко", d["apple"]);
    }

    TEST(OperatorMinusEquals_RemoveWord)
    {
        Dict d;
        d += { "dog", "собака" };
        CHECK_EQUAL("собака", d["dog"]);
        d -= { "dog", "собака" };
        CHECK_EQUAL("<отсутствует>", d["dog"]);
    }

    TEST(OperatorMinusEquals_RemoveNonexistentWord)
    {
        Dict d;
        d += { "dog", "собака" };
        d -= { "cat", "кот" }; // нет такого ключа
        CHECK_EQUAL("собака", d["dog"]); // существующий элемент не должен трогаться
    }

    TEST(OperatorIndex_Const)
    {
        Dict d;
        d += { "tree", "дерево" };
        const Dict& cd = d;
        CHECK_EQUAL("дерево", cd["tree"]);
        CHECK_EQUAL("<отсутствует>", cd["house"]);
    }

    TEST(OperatorIndex_NonConst_AddsMissingWord)
    {
        Dict d;
        string& ref = d["book"];
        CHECK_EQUAL("<отсутствует>", ref);
        ref = "книга";
        CHECK_EQUAL("книга", d["book"]);
    }

    TEST(CopyConstructor)
    {
        Dict d1;
        d1 += { "one", "один" };
        d1 += { "two", "два" };

        Dict d2 = d1;
        CHECK_EQUAL("один", d2["one"]);
        CHECK_EQUAL("два", d2["two"]);

        d2["one"] = "Один!";
        CHECK_EQUAL("один", d1["one"]); // проверка глубокого копирования
    }

    TEST(AssignmentOperator)
    {
        Dict d1;
        d1 += { "sun", "солнце" };
        Dict d2;
        d2 += { "moon", "луна" };

        d2 = d1;
        CHECK_EQUAL("солнце", d2["sun"]);
        CHECK_EQUAL("<отсутствует>", d2["moon"]);

        d2 = d2;
        CHECK_EQUAL("солнце", d2["sun"]);
    }

    TEST(StreamOperators_SaveAndLoad)
    {
        Dict d1;
        d1 += { "apple", "яблоко" };
        d1 += { "cat", "кот" };

        std::stringstream ss;
        ss << d1;

        Dict d2;
        ss >> d2;

        CHECK_EQUAL("яблоко", d2["apple"]);
        CHECK_EQUAL("кот", d2["cat"]);
    }

    // Новые тесты для покрытия дерева
    TEST(MultipleInsertions_AndTreeStructure)
    {
        Dict d;
        d += { "mouse", "мышь" };
        d += { "cat", "кот" };
        d += { "tree", "дерево" };
        d += { "apple", "яблоко" };
        d += { "zebra", "зебра" };

        TreeNode* root = d.getRoot();
        CHECK(root != nullptr);
        CHECK_EQUAL("mouse", root->getWords().first);
        CHECK_EQUAL("cat", root->getLeft()->getWords().first);
        CHECK_EQUAL("tree", root->getRight()->getWords().first);
        CHECK_EQUAL("apple", root->getLeft()->getLeft()->getWords().first);
        CHECK_EQUAL("zebra", root->getRight()->getRight()->getWords().first);
    }

    TEST(RemoveNodeWithTwoChildren)
    {
        Dict d;
        d += { "mouse", "мышь" };
        d += { "cat", "кот" };
        d += { "tree", "дерево" };
        d += { "apple", "яблоко" };
        d += { "zebra", "зебра" };

        d -= { "mouse", "мышь" }; // корень с двумя детьми

        TreeNode* root = d.getRoot();
        CHECK(root != nullptr);
        CHECK(root->getWords().first != "mouse"); // корень заменён
        CHECK_EQUAL("cat", root->getLeft()->getWords().first);
        CHECK_EQUAL("tree", root->getWords().first);
    }

    TEST(NodeCount_AfterInsertionsAndDeletions)
    {
        Dict d;
        CHECK_EQUAL(0, d.getRoot() ? d.getRoot()->nodeCount() : 0);

        d += { "m", "эм" };
        d += { "c", "цэ" };
        d += { "t", "тэ" };
        d += { "a", "а" };

        CHECK_EQUAL(4, d.getRoot()->nodeCount());

        d -= { "c", "цэ" };
        CHECK_EQUAL(3, d.getRoot()->nodeCount());
    }
}

int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    return UnitTest::RunAllTests();
}
