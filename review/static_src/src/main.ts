import APIClient from './api';
import {Annotation, AnnotatableSection} from './annotation';
import {Comment, CommentReply} from './types';

import './comments.css';

declare var Vue;


function initCommentsApp(element: HTMLElement, api: APIClient) {
    let app = new Vue({
        el: element,
        data: {
            api,
            nextId: 0,
            comments: [],
            commentableSections: {},
        },
        methods: {
            newComment(annotation: Annotation) {
                let commentId = this.nextId++;
                this.comments.push(Comment.makeNew(commentId, annotation));
                this.updateLayout();

                // Set focus in text area
                this.$nextTick(function() {
                    let textarea = this.$el.querySelector(`[data-comment-id="${commentId}"] input[type="textarea"]`);
                    textarea.focus();
                });
            },
            addComment(comment: Comment) {
                let onSubmitted = () => {
                    this.updateLayout();
                };

                comment.save(this.api).then(onSubmitted);
            },
            cancelComment(comment: Comment) {
                let index = this.comments.indexOf(comment);
                this.comments.splice(index, 1);
                this.updateLayout();

                comment.delete(null);
            },
            deleteComment(comment: Comment) {
                let onDeleted = () => {
                    let index = this.comments.indexOf(comment);
                    this.comments.splice(index, 1);
                    this.updateLayout();
                }

                comment.delete(this.api).then(onDeleted);
            },
            sendReply(comment: Comment) {
                let reply = new CommentReply(comment.newReply);
                comment.replies.push(reply);

                comment.newReply = '';
            },
            async fetchComments() {
                let response = await fetch(`${this.api.baseUrl}/comments/`, {
                    headers: {
                        'X-Review-Token': this.api.reviewToken,
                    }
                });

                let comments = await response.json();

                for (let comment of comments) {
                    let section = this.commentableSections[comment.content_path];
                    if (!section) {
                        continue
                    }

                    let annotation = section.addAnnotation({
                        quote: comment.quote,
                        ranges: [{
                            start: comment.start_xpath || '.', // FIXME: TEMPORARY
                            startOffset: comment.start_offset,
                            end: comment.end_xpath || '.', // FIXME: TEMPORARY
                            endOffset: comment.end_offset,
                        }]
                    });

                    this.comments.push(Comment.fromApi(this.nextId++, annotation, comment));
                    this.updateLayout();
                }
            },
            addCommentableSection(contentPath, element) {
                this.commentableSections[contentPath] = new AnnotatableSection(contentPath, element, this.newComment);
            },
            updateLayout() {
                const GAP = 20.0;  // Gap between comments in pixels
                const TOP_MARGIN = 100.0;  // Spacing from the top to the first comment in pixels

                this.$nextTick(function() {
                    let commentElements: {[commentId: string]: HTMLElement} = {};
                    let commentPositions: {[commentId: string]: number} = {};
                    let commentHeights: {[commentId: string]: number} = {};

                    for (let comment of this.comments) {
                        let element = comment.getElement(this.$el);

                        if (element) {
                            let desiredPosition = comment.getDesiredPosition();

                            // FIXME: this should never happen
                            if (desiredPosition !== undefined) {
                                commentElements[comment.id] = element;
                                commentPositions[comment.id] = desiredPosition;
                                commentHeights[comment.id] = element.offsetHeight;
                            }
                        }
                    }

                    interface Block {
                        position: number,
                        height: number,
                        comments: string[],
                    }

                    // Build initial list of blocks
                    let blocks: Block[] = [];
                    for (let commentId in commentElements) {
                        blocks.push({
                            position: commentPositions[commentId],
                            height: commentHeights[commentId],
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

    app.fetchComments();

    return app;
}

window['CommentsAPI'] = APIClient;
window['initCommentsApp'] = initCommentsApp;
