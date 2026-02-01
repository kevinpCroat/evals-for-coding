"""
Comprehensive test suite for tree traversal operations.
All tests must pass after rewriting to iterative implementations.
"""

import pytest
from tree_traversal import (
    TreeNode,
    inorder_traversal,
    postorder_traversal,
    max_depth,
    find_path_sum,
    collect_leaves,
    tree_map
)


class TestInorderTraversal:
    """Test cases for inorder traversal."""

    def test_empty_tree(self):
        """Empty tree should return empty list."""
        assert inorder_traversal(None) == []

    def test_single_node(self):
        """Single node tree."""
        root = TreeNode(1)
        assert inorder_traversal(root) == [1]

    def test_left_skewed_tree(self):
        """Tree with only left children."""
        root = TreeNode(3, TreeNode(2, TreeNode(1)))
        assert inorder_traversal(root) == [1, 2, 3]

    def test_right_skewed_tree(self):
        """Tree with only right children."""
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
        assert inorder_traversal(root) == [1, 2, 3]

    def test_balanced_tree(self):
        """Balanced binary tree."""
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        root = TreeNode(1,
                       TreeNode(2, TreeNode(4), TreeNode(5)),
                       TreeNode(3))
        assert inorder_traversal(root) == [4, 2, 5, 1, 3]

    def test_complex_tree(self):
        """More complex tree structure."""
        #         5
        #        / \
        #       3   7
        #      / \ / \
        #     2  4 6  8
        root = TreeNode(5,
                       TreeNode(3, TreeNode(2), TreeNode(4)),
                       TreeNode(7, TreeNode(6), TreeNode(8)))
        assert inorder_traversal(root) == [2, 3, 4, 5, 6, 7, 8]


class TestPostorderTraversal:
    """Test cases for postorder traversal."""

    def test_empty_tree(self):
        """Empty tree should return empty list."""
        assert postorder_traversal(None) == []

    def test_single_node(self):
        """Single node tree."""
        root = TreeNode(1)
        assert postorder_traversal(root) == [1]

    def test_left_skewed_tree(self):
        """Tree with only left children."""
        root = TreeNode(3, TreeNode(2, TreeNode(1)))
        assert postorder_traversal(root) == [1, 2, 3]

    def test_right_skewed_tree(self):
        """Tree with only right children."""
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
        assert postorder_traversal(root) == [3, 2, 1]

    def test_balanced_tree(self):
        """Balanced binary tree."""
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        root = TreeNode(1,
                       TreeNode(2, TreeNode(4), TreeNode(5)),
                       TreeNode(3))
        assert postorder_traversal(root) == [4, 5, 2, 3, 1]


class TestMaxDepth:
    """Test cases for maximum depth calculation."""

    def test_empty_tree(self):
        """Empty tree has depth 0."""
        assert max_depth(None) == 0

    def test_single_node(self):
        """Single node has depth 1."""
        root = TreeNode(1)
        assert max_depth(root) == 1

    def test_two_levels(self):
        """Tree with two levels."""
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        assert max_depth(root) == 2

    def test_left_skewed_depth(self):
        """Deep left-skewed tree."""
        root = TreeNode(1,
                       TreeNode(2,
                               TreeNode(3,
                                       TreeNode(4))))
        assert max_depth(root) == 4

    def test_unbalanced_tree(self):
        """Unbalanced tree - max depth on right side."""
        root = TreeNode(1,
                       TreeNode(2),
                       TreeNode(3,
                               None,
                               TreeNode(4,
                                       None,
                                       TreeNode(5))))
        assert max_depth(root) == 4


class TestFindPathSum:
    """Test cases for path sum finding."""

    def test_empty_tree(self):
        """Empty tree has no paths."""
        assert find_path_sum(None, 0) == False
        assert find_path_sum(None, 10) == False

    def test_single_node_match(self):
        """Single node matching target."""
        root = TreeNode(5)
        assert find_path_sum(root, 5) == True

    def test_single_node_no_match(self):
        """Single node not matching target."""
        root = TreeNode(5)
        assert find_path_sum(root, 10) == False

    def test_path_exists_left(self):
        """Path sum exists on left side."""
        #       5
        #      / \
        #     4   8
        #    /   / \
        #   11  13  4
        #  /  \      \
        # 7    2      1
        root = TreeNode(5,
                       TreeNode(4,
                               TreeNode(11,
                                       TreeNode(7),
                                       TreeNode(2))),
                       TreeNode(8,
                               TreeNode(13),
                               TreeNode(4,
                                       None,
                                       TreeNode(1))))
        assert find_path_sum(root, 22) == True  # 5->4->11->2

    def test_path_exists_right(self):
        """Path sum exists on right side."""
        root = TreeNode(5,
                       TreeNode(4,
                               TreeNode(11,
                                       TreeNode(7),
                                       TreeNode(2))),
                       TreeNode(8,
                               TreeNode(13),
                               TreeNode(4,
                                       None,
                                       TreeNode(1))))
        assert find_path_sum(root, 18) == True  # 5->8->4->1

    def test_path_not_exists(self):
        """Path sum does not exist."""
        root = TreeNode(1,
                       TreeNode(2),
                       TreeNode(3))
        assert find_path_sum(root, 10) == False

    def test_negative_values(self):
        """Tree with negative values."""
        root = TreeNode(1,
                       TreeNode(-2,
                               TreeNode(3)),
                       TreeNode(-3))
        assert find_path_sum(root, 2) == True  # 1->-2->3
        assert find_path_sum(root, -2) == True  # 1->-3


class TestCollectLeaves:
    """Test cases for collecting leaf nodes."""

    def test_empty_tree(self):
        """Empty tree has no leaves."""
        assert collect_leaves(None) == []

    def test_single_node(self):
        """Single node is a leaf."""
        root = TreeNode(1)
        assert collect_leaves(root) == [1]

    def test_two_leaves(self):
        """Tree with two leaves."""
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        assert collect_leaves(root) == [2, 3]

    def test_left_to_right_order(self):
        """Leaves collected in left-to-right order."""
        #       1
        #      / \
        #     2   3
        #    / \   \
        #   4   5   6
        root = TreeNode(1,
                       TreeNode(2,
                               TreeNode(4),
                               TreeNode(5)),
                       TreeNode(3,
                               None,
                               TreeNode(6)))
        assert collect_leaves(root) == [4, 5, 6]

    def test_complex_tree_leaves(self):
        """More complex tree."""
        #         1
        #        / \
        #       2   3
        #      /   / \
        #     4   5   6
        #    /         \
        #   7           8
        root = TreeNode(1,
                       TreeNode(2,
                               TreeNode(4,
                                       TreeNode(7))),
                       TreeNode(3,
                               TreeNode(5),
                               TreeNode(6,
                                       None,
                                       TreeNode(8))))
        assert collect_leaves(root) == [7, 5, 8]


class TestTreeMap:
    """Test cases for tree mapping function."""

    def test_empty_tree(self):
        """Mapping empty tree returns None."""
        result = tree_map(None, lambda x: x * 2)
        assert result is None

    def test_single_node_map(self):
        """Map function to single node."""
        root = TreeNode(5)
        result = tree_map(root, lambda x: x * 2)
        assert result.val == 10
        assert result.left is None
        assert result.right is None

    def test_simple_tree_map(self):
        """Map function to simple tree."""
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        result = tree_map(root, lambda x: x * 2)
        assert result.val == 2
        assert result.left.val == 4
        assert result.right.val == 6

    def test_complex_tree_map(self):
        """Map function to complex tree."""
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        root = TreeNode(1,
                       TreeNode(2, TreeNode(4), TreeNode(5)),
                       TreeNode(3))
        result = tree_map(root, lambda x: x + 10)
        assert result.val == 11
        assert result.left.val == 12
        assert result.left.left.val == 14
        assert result.left.right.val == 15
        assert result.right.val == 13

    def test_map_preserves_structure(self):
        """Mapping preserves tree structure."""
        root = TreeNode(1,
                       TreeNode(2, TreeNode(4)),
                       TreeNode(3, None, TreeNode(5)))
        result = tree_map(root, lambda x: -x)

        # Check structure is preserved
        assert result.left.left is not None
        assert result.left.right is None
        assert result.right.left is None
        assert result.right.right is not None

    def test_map_different_function(self):
        """Test with different mapping function."""
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        result = tree_map(root, lambda x: x ** 2)
        assert result.val == 1
        assert result.left.val == 4
        assert result.right.val == 9


# Edge case tests - explicitly defined
class TestEdgeCases:
    """Explicit edge case tests for verification scoring."""

    def test_deep_recursion_inorder(self):
        """Test with deep tree (100+ levels) - tests stack depth handling."""
        # Create a deep left-skewed tree
        root = TreeNode(100)
        current = root
        for i in range(99, 0, -1):
            current.left = TreeNode(i)
            current = current.left

        result = inorder_traversal(root)
        assert result == list(range(1, 101))
        assert len(result) == 100

    def test_deep_recursion_max_depth(self):
        """Test max_depth with very deep tree."""
        root = TreeNode(1)
        current = root
        for i in range(99):
            current.right = TreeNode(i + 2)
            current = current.right

        assert max_depth(root) == 100

    def test_path_sum_with_zero(self):
        """Edge case: path sum with zero values."""
        root = TreeNode(0, TreeNode(0), TreeNode(0))
        assert find_path_sum(root, 0) == True

    def test_large_tree_leaves(self):
        """Edge case: collect leaves from large tree."""
        # Create a complete binary tree of depth 5
        def create_complete_tree(val, depth):
            if depth == 0:
                return None
            node = TreeNode(val)
            node.left = create_complete_tree(val * 2, depth - 1)
            node.right = create_complete_tree(val * 2 + 1, depth - 1)
            return node

        root = create_complete_tree(1, 5)
        leaves = collect_leaves(root)
        # Complete binary tree of depth 5 has 16 leaves
        assert len(leaves) == 16

    def test_tree_map_identity(self):
        """Edge case: tree_map with identity function."""
        root = TreeNode(1,
                       TreeNode(2, TreeNode(4), TreeNode(5)),
                       TreeNode(3))
        result = tree_map(root, lambda x: x)
        # Should create identical tree
        assert inorder_traversal(result) == inorder_traversal(root)
