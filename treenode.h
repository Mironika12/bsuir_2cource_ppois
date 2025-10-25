#pragma once
#include <iostream>
using namespace std;

class TreeNode {
public:
	TreeNode* getLeft() const;
	TreeNode* getRight() const;
	pair<string, string> getPair() const;
	string& getRuAdress();
	void setLeft(TreeNode*);
	void setRight(TreeNode*);
	void setPair(pair<string, string>);
	TreeNode* remove(pair<string, string>);
	TreeNode* insert(pair<string, string>);
	TreeNode* find(string);
	void clear();
	//pair<string, string> split(string, char);
	int nodeCount();
	//TreeNode();
	TreeNode(pair<string, string> words);
	//~TreeNode();
	bool operator==(const TreeNode& other) const;
	bool operator!=(const TreeNode& other) const;
	//TreeNode(const TreeNode& other); // конструктор копирования
	//TreeNode& operator=(const TreeNode& other); // оператор присваивания
private:
	TreeNode* left_, * right_;
	pair<string, string> words_;
};
