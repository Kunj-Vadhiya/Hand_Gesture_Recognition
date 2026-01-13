"""
MediaPipe Python 3.13 Compatibility Patch
Fixes the ctypes 'free' function issue
"""

import ctypes
import ctypes.util
import sys


def patch_mediapipe_for_python313():
    """
    Patch MediaPipe to work with Python 3.13
    by fixing the ctypes.CDLL 'free' attribute access issue
    """
    if sys.version_info >= (3, 13):
        # Store original CDLL
        original_cdll = ctypes.CDLL
        
        class PatchedCDLL(original_cdll):
            """Patched CDLL that handles missing 'free' function"""
            
            def __getattr__(self, name):
                try:
                    return super().__getattr__(name)
                except AttributeError:
                    if name == 'free':
                        # Create a dummy free function
                        # Get libc
                        if sys.platform == 'win32':
                            libc = ctypes.CDLL('msvcrt', use_errno=True)
                        else:
                            libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
                        
                        # Return libc's free if available
                        if hasattr(libc, 'free'):
                            return libc.free
                        else:
                            # Create dummy free function
                            @ctypes.CFUNCTYPE(None, ctypes.c_void_p)
                            def dummy_free(ptr):
                                pass
                            return dummy_free
                    raise
        
        # Replace CDLL with patched version
        ctypes.CDLL = PatchedCDLL
        print("✓ Applied Python 3.13 compatibility patch for MediaPipe")
        return True
    return False


# Apply patch before importing mediapipe
patch_mediapipe_for_python313()
