#pragma once
#include <iostream>
#include "treenode.h"
using namespace std;

/**
 * @class Dict
 * @brief English–Russian dictionary implemented using a binary search tree.
 *
 * Provides methods for adding, removing, and searching words, as well as
 * tree manipulation via overloaded operators.
 */
class Dict {
public:
    /**
     * @brief Add a new word pair to the dictionary.
     *
     * Inserts the element into the tree if the word does not already exist.
     *
     * @param wordPair Pair <English word, translation>.
     * @return Reference to the current object.
     */
    Dict& operator +=(const pair<string, string>& wordPair);

    /**
     * @brief Remove a word from the dictionary.
     *
     * Removal is based on the English word.
     *
     * @param words Pair containing the key to remove.
     * @return Reference to the current object.
     */
    Dict& operator -=(const pair<string, string>& words);

    /**
     * @brief Get the translation of a word (const version).
     *
     * If the word is not found, returns "<missing>".
     *
     * @param en English word.
     * @return Translation string.
     */
    string operator[](const string& en) const;

    /**
     * @brief Get or create a translation (non-const version).
     *
     * If the word is not found, it is inserted with the value "<missing>".
     *
     * @param en English word.
     * @return Reference to the translation string (modifiable).
     */
    string& operator[](const string& en);

    /**
     * @brief Check whether the dictionary is empty.
     * @return true if the tree root is null.
     */
    bool empty();

    /**
     * @brief Get the root node of the tree.
     * @return Pointer to the root.
     */
    TreeNode* getRoot();

    /**
     * @brief Construct an empty dictionary.
     */
    Dict();

    /**
     * @brief Construct a dictionary with one word.
     * @param words Pair <English word, translation>.
     */
    Dict(pair<string, string> words);

    /**
     * @brief Destructor. Deletes the entire tree.
     */
    ~Dict();

    /**
     * @brief Copy constructor.
     * @param other Another dictionary.
     */
    Dict(const Dict& other);

    /**
     * @brief Assignment operator.
     * @param other Another dictionary.
     * @return Reference to the current object.
     */
    Dict& operator=(const Dict& other);

    /**
     * @brief Serialize the dictionary into an output stream.
     *
     * Outputs the tree in preorder using "NULL" for empty nodes.
     */
    friend std::ostream& operator<<(std::ostream& os, const Dict& dict);

    /**
     * @brief Load the dictionary from an input stream.
     *
     * The format must match outputDict().
     */
    friend std::istream& operator>>(std::istream& is, Dict& dict);

    /**
     * @brief Recursively output the tree to a stream.
     * @param os Output stream.
     * @param node Current node.
     */
    void outputDict(std::ostream& os, TreeNode* node) const;

    /**
     * @brief Recursively load the tree from a stream.
     * @param is Input stream.
     * @return Root of the loaded subtree.
     */
    TreeNode* inputDict(std::istream& is);

private:
    TreeNode* root; ///< Dictionary tree root
};
