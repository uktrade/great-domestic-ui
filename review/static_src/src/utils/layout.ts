import {Annotation} from './annotation';

const GAP = 20.0;  // Gap between comments in pixels
const TOP_MARGIN = 100.0;  // Spacing from the top to the first comment in pixels

export class LayoutController {
    commentElements: {[commentId: number]: HTMLElement} = {};
    commentAnnotations: {[commentId: number]: Annotation} = {};
    commentDesiredPositions: {[commentId: number]: number} = {};
    commentHeights: {[commentId: number]: number} = {};
    commentCalculatedPositions: {[commentId: number]: number} = {};
    isDirty: boolean = false;

    setCommentElement(commentId: number, element: HTMLElement) {
        if (element) {
            console.log("SET ELEMENT", commentId);
            this.commentElements[commentId] = element;
        } else {
            console.log("DELETE ELEMENT", commentId);
            delete this.commentElements[commentId];
        }

        this.isDirty = true;
    }

    setCommentAnnotation(commentId: number, annotation: Annotation) {
        console.log("SET COMMENT ANNOTATION", commentId)
        this.commentAnnotations[commentId] = annotation;
        this.updateDesiredPosition(commentId);
        this.isDirty = true;
    }

    setCommentHeight(commentId: number, height: number) {
        if (this.commentHeights[commentId] != height) {
            this.commentHeights[commentId] = height;
            this.isDirty = true;

            console.log("SET COMMENT HEIGHT", commentId, height)

        }
    }

    updateDesiredPosition(commentId: number) {
        let annotation = this.commentAnnotations[commentId];

        let sum = 0;
        let count = 0;
        for (let highlight of annotation.highlights) {
            sum += highlight.offsetTop;
            count++;
        }

        if (count == 0) {
            return;
        }

        console.log("SET COMMENT POSITION", commentId, sum / count)

        this.commentDesiredPositions[commentId] = sum / count;
    }

    refresh() {
        if (!this.isDirty) {
            return;
        }

        interface Block {
            position: number,
            height: number,
            comments: string[],
        }

        // Build list of blocks (starting with one for each comment)
        let blocks: Block[] = [];
        for (let commentId in this.commentElements) {
            blocks.push({
                position: this.commentDesiredPositions[commentId],
                height: this.commentHeights[commentId],
                comments: [commentId],
            })
        }

        // Sort blocks
        blocks.sort((a, b) => a.position - b.position);

        // Resolve overlapping blocks
        let overlaps = true;
        while (overlaps) {
            overlaps = false;
            let newBlocks: Block[] = [];
            let previousBlock: Block|null = null;

            for (let block of blocks) {
                if (previousBlock) {
                    if (previousBlock.position + previousBlock.height + GAP > block.position) {
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

        // Write positions
        for (let block of blocks) {
            let currentPosition = block.position;
            for (let commentId of block.comments) {
                this.commentCalculatedPositions[commentId] = currentPosition;
                currentPosition += this.commentHeights[commentId] + GAP;
            }
        }

        this.isDirty = false;
    }

    getCommentPosition(commentId: number) {
        if (commentId in this.commentCalculatedPositions) {
            return this.commentCalculatedPositions[commentId];
        } else {
            return this.commentDesiredPositions[commentId];
        }
    }
}


