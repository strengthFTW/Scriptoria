# File Upload Loading State

## Changes
1.  **Modified `frontend/src/index.css`**:
    - Added `.spinner` class with a simple CSS rotation animation.
    - Added `@keyframes spin`.

2.  **Modified `frontend/src/App.jsx`**:
    - In the `upload-box` div, added a conditional check for `isUploading`.
    - If `isUploading` is true:
        - Replaced the upload icon (svg) with `<div className="spinner" />`.
        - Changed the primary text to "Uploading...".
        - Changed the secondary text to show the upload progress percentage in red.
    - If `isUploading` is false:
        - Restored the original icon and text behavior (showing "Uploaded Successfully" if a file is present).

## Verification
- Ran `npm run build` in `frontend` directory, which passed successfully.
