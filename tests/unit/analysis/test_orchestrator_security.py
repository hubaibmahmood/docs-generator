import unittest
from unittest.mock import patch, MagicMock
import os
from src.analysis.orchestrator import AnalysisOrchestrator

class TestOrchestratorSecurity(unittest.TestCase):

    @patch('src.analysis.orchestrator.os.walk')
    @patch('src.analysis.orchestrator.os.path.islink')
    @patch('src.analysis.orchestrator.ParserFactory.get_parser')
    @patch('builtins.open', new_callable=MagicMock)
    def test_analyze_local_path_skips_symlinks(self, mock_open, mock_get_parser, mock_islink, mock_walk):
        # Arrange
        orchestrator = AnalysisOrchestrator()
        base_path = "/tmp/test_repo"
        
        # Mock os.walk to return one directory with a symlinked subdir and a symlinked file
        # structure:
        # /tmp/test_repo
        #   - valid_dir/
        #   - symlink_dir -> /etc
        #   - valid_file.py
        #   - symlink_file.py -> /etc/passwd
        
        mock_walk.return_value = [
            (base_path, ["valid_dir", "symlink_dir"], ["valid_file.py", "symlink_file.py"])
        ]
        
        # Mock islink logic
        def islink_side_effect(path):
            if path.endswith("symlink_dir"):
                return True
            if path.endswith("symlink_file.py"):
                return True
            return False
        
        mock_islink.side_effect = islink_side_effect
        
        # Act
        result = orchestrator.analyze_local_path(base_path)
        
        # Assert
        # 1. Symlink directory "symlink_dir" should be removed from dirs list during walk
        # The orchestrator modifies the list in-place, so we check if it was called correctly
        # or check the resulting file tree.
        
        # Check file tree
        children = result.file_tree['children']
        names = [child['name'] for child in children]
        
        self.assertIn("valid_file.py", names)
        self.assertNotIn("symlink_dir", names)
        # Note: symlink_file.py might appear in the loop but should NOT be parsed/analyzed
        
        # Check that parser was ONLY called for valid_file.py
        # get_parser is called for all files in the 'files' list of os.walk
        # BUT our logic should verify if it's a link before doing heavy lifting or adding to tree?
        # Let's re-read the implementation we wrote.
        # "Skip file symlinks... continue"
        
        # So get_parser shouldn't be called for symlink_file.py? 
        # Wait, `ParserFactory.get_parser(file_path)` is called AFTER the symlink check in our new code?
        # Let's verify the implementation order in `orchestrator.py`
        
        # Implementation:
        # for file_name in files:
        #   file_path = ...
        #   if os.path.islink(file_path): continue
        #   parser = ParserFactory.get_parser(file_path)
        
        # So get_parser should NOT be called for symlink_file.py
        valid_file_path = os.path.join(base_path, "valid_file.py")
        symlink_file_path = os.path.join(base_path, "symlink_file.py")
        
        mock_get_parser.assert_called_with(valid_file_path)
        
        # Verify it was NOT called with symlink_file.py
        # We iterate over all calls to confirm
        for call in mock_get_parser.call_args_list:
            self.assertNotEqual(call[0][0], symlink_file_path, "Parser should not be called for symlink file")

if __name__ == '__main__':
    unittest.main()
