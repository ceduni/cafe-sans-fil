let root = null

export function getRoot() {
    return root;
}

export function setRoot(value) {
    if (root !== null) {
        throw new Error('Root has already been set.');
    }
    root = value;
}