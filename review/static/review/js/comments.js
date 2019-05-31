class BaseComment {
    constructor(id, ann, highlights) {
        this.id = id;
        this.ann = ann;
        this.highlights = highlights;

        this._element = null;
    }

    getDesiredPosition() {
        return this.highlights[0].getBoundingClientRect().top + window.scrollY;
    }

    getElement(containerElement) {
        if (!this._element) {
            this._element = document.querySelector(`[data-comment-id="${this.id}"]`);
        }

        return this._element;
    }
}

class Comment extends BaseComment {
    constructor(id, text, ann, highlights) {
        super(id, ann, highlights);

        this.author = "AUTHOR";
        this.text = text;
        this.highlights = highlights;
    }

    getDateDisplay() {
        return "DATE";
    }
}

class NewComment extends BaseComment {
    constructor(id, contentPath, ann, highlights) {
        super(id, ann, highlights);
        this.text = "";
        this.isNew = true;
        this.highlights = highlights;
    }

    intoComment() {
        return new Comment(this.id, this.text, this.ann, this.highlights);
    }
}

class CommentsApp {
    constructor(element, apiBase) {
        this.element = element;
        this.apiBase = apiBase;

        this.vue = new Vue({
            el: element,
            data: {
                nextId: 0,
                comments: [],
            },
            methods: {
                addComment(comment) {
                    let index = this.comments.indexOf(comment);
                    this.$set(this.comments, index, comment.intoComment());
                    this.updateLayout();
                },
                cancelComment(comment) {
                    let index = this.comments.indexOf(comment);
                    this.comments.splice(index);
                    this.updateLayout();
                },
                updateLayout() {
                    const GAP = 20.0;  // Gap between comments in pixels
                    const TOP_MARGIN = 100.0;  // Spacing from the top to the first comment in pixels

                    this.$nextTick(function() {
                        let commentElements = {};
                        let commentPositions = {};
                        let commentHeights = {};

                        for (let comment of this.comments) {
                            let element = comment.getElement(this.$el);

                            if (element) {
                                commentElements[comment.id] = element;
                                commentPositions[comment.id] = comment.getDesiredPosition();
                                commentHeights[comment.id] = element.offsetHeight;
                            }
                        }

                        // Build initial list of blocks
                        let blocks = [];
                        for (let commentId in commentElements) {
                            blocks.push({
                                position: commentPositions[commentId],
                                height: commentHeights[commentId] + GAP,
                                comments: [commentId],
                            })
                        }

                        // Sort blocks
                        blocks.sort((a, b) => a.position - b.position);

                        // Resolve overlapping blocks
                        let overlaps = true;
                        while (overlaps) {
                            overlaps = false;
                            let newBlocks = [];
                            let previousBlock = null;

                            for (let block of blocks) {
                                if (previousBlock) {
                                    if (previousBlock.position + previousBlock.height > block.position) {
                                        overlaps = true;

                                        // Merge the blocks
                                        previousBlock.height += block.height;
                                        previousBlock.comments.push(...block.comments);

                                        // Move the block so it balances across all comments within it
                                        /* FIXME: Doesn't handle some edge cases well yet
                                        let shift = 0.0;
                                        let currentPosition = previousBlock.position;
                                        for (let commentId of previousBlock.comments) {
                                            let desiredPosition = commentPositions[commentId];
                                            shift += desiredPosition - currentPosition;
                                            currentPosition += commentHeights[commentId];
                                        }
                                        previousBlock.position += shift;
                                        if (previousBlock.position < TOP_MARGIN) {
                                            previousBlock.position = TOP_MARGIN;
                                        }
                                        */
                                        continue;
                                    }
                                }

                                newBlocks.push(block);
                                previousBlock = block;
                            }

                            blocks = newBlocks;
                        }

                        // Copy positions into the DOM
                        for (let block of blocks) {
                            let currentPosition = block.position;
                            for (let commentId of block.comments) {
                                commentElements[commentId].style.top = `${currentPosition}px`;
                                currentPosition += commentHeights[commentId] + GAP;
                            }
                        }
                    })
                }
            },
        });
    }

    startNewComment(contentPath, ann, highlights) {
        this.vue.comments.push(new NewComment(this.vue.nextId++, contentPath, ann, highlights));
        this.vue.updateLayout();
    }
}
