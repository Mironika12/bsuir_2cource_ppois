#pragma once
#include <iostream>
using namespace std;

/**
 * @class TreeNode
 * @brief A node of a binary search tree storing a pair "English word — translation".
 *
 * Each node contains the word, its translation, and pointers to the left and right children.
 * Used to implement the dictionary as a binary search tree.
 */
class TreeNode {
public:
    /**
     * @brief Get a pointer to the left child node.
     * @return Pointer to the left child or nullptr.
     */
    TreeNode* getLeft() const;

    /**
     * @brief Get a pointer to the right child node.
     * @return Pointer to the right child or nullptr.
     */
    TreeNode* getRight() const;

    /**
     * @brief Get the stored word pair (const version).
     * @return Reference to the pair <English word, translation>.
     */
    const pair<string, string>& getWords() const;

    /**
     * @brief Get the stored word pair (non-const version).
     * @return Reference to the pair <English word, translation>.
     */
    pair<string, string>& getWords();

    /**
     * @brief Set the left child node.
     * @param left Pointer to the new left child.
     */
    void setLeft(TreeNode* left);

    /**
     * @brief Set the right child node.
     * @param right Pointer to the new right child.
     */
    void setRight(TreeNode* right);

    /**
     * @brief Set a new word pair.
     * @param words Pair <English word, translation>.
     */
    void setWords(pair<string, string> words);

    /**
     * @brief Remove a node with the given word pair from the subtree.
     *
     * Removal is based on the key (the English word).
     * Returns the new root of the subtree.
     *
     * @param words Pair containing the key to remove.
     * @return New root of the subtree after removal.
     */
    TreeNode* remove(pair<string, string> words);

    /**
     * @brief Insert a new word pair into the subtree.
     *
     * Inserts a new element into the binary search tree.
     * Returns the root of the current subtree.
     *
     * @param words Pair <English word, translation>.
     * @return Pointer to the current node (subtree root).
     */
    TreeNode* insert(pair<string, string> words);

    /**
     * @brief Find a node by the English word.
     * @param en English word.
     * @return Pointer to the found node or nullptr.
     */
    TreeNode* find(string en);

    /**
     * @brief Count the number of nodes in the subtree.
     * @return Total number of nodes including the current one.
     */
    int nodeCount();

    /**
     * @brief Constructor.
     * @param words Pair <English word, translation>.
     */
    TreeNode(pair<string, string> words);

    /**
     * @brief Compare two nodes for equality.
     * @param other Another node.
     * @return true if both nodes store the same pair.
     */
    bool operator==(const TreeNode& other) const;

    /**
     * @brief Compare two nodes for inequality.
     * @param other Another node.
     * @return true if the pairs differ.
     */
    bool operator!=(const TreeNode& other) const;

    /**
     * @brief Destructor. Recursively deletes child nodes.
     */
    ~TreeNode();

private:
    TreeNode* left_;   ///< Left child
    TreeNode* right_;  ///< Right child
    pair<string, string> words_; ///< Stored pair "word — translation"
};
