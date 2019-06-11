import * as React from 'react';
import * as ReactDOM from 'react-dom';

import {Author, Comment, CommentReply, Store} from '../../state';
import {updateComment, deleteComment, setFocusedComment, addReply, updateReply} from '../../actions';
import APIClient from '../../api';
import {LayoutController} from '../../utils/layout';
import {getNextReplyId} from '../../utils/sequences';
import CommentReplyComponent from '../CommentReply';

import './style.scss';

export interface CommentProps {
    store: Store,
    comment: Comment,
    api: APIClient,
    layout: LayoutController,
    defaultAuthor: Author,
}

export default class CommentComponent extends React.Component<CommentProps> {
    renderHeader() {
        let { comment, store, api } = this.props;
        let title, date, resolved;

        if (comment.mode == 'creating') {
            title = "New comment";
            date = "";
            resolved = <></>;
        } else {
            title = comment.author.name;
            date = "10:25 May 10";

            let toggleResolved = async (e: React.MouseEvent) => {
                e.preventDefault();

                let isResolved = !comment.isResolved;

                store.dispatch(updateComment(comment.localId, {
                    isResolved,
                    updatingResolvedStatus: true,
                }));

                await api.saveCommentResolvedStatus(comment, isResolved);

                store.dispatch(updateComment(comment.localId, {
                    updatingResolvedStatus: false,
                }));
            };

            resolved = <div className="comment__header-resolved">
                <label htmlFor="resolved">Resolved</label>
                <input name="resolved" type="checkbox" onClick={toggleResolved} checked={comment.isResolved} />
            </div>;
        }

        return <div className="comment__header">
            <div className="comment__header-info">
                <h2>{title}</h2>
                <p className="comment__date">{date}</p>
            </div>
            {resolved}
        </div>;
    }

    renderReplies() {
        let { comment, store, api, defaultAuthor } = this.props;

        if (!comment.remoteId) {
            // Hide replies UI if the comment itself isn't saved yet
            return <></>;
        }

        let onChangeNewReply = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                newReply: e.target.value,
            }));
        };

        let onClickSendReply = async (e: React.MouseEvent) => {
            e.preventDefault();

            let replyId = getNextReplyId();
            let reply = new CommentReply(replyId, defaultAuthor, {text: comment.newReply, mode: 'saving'});
            store.dispatch(addReply(comment.localId, reply));

            store.dispatch(updateComment(comment.localId, {
                newReply: '',
            }));

            let replyData = await api.saveCommentReply(comment, reply);

            store.dispatch(updateReply(comment.localId, replyId, {
                remoteId: replyData.id,
                mode: 'default',
                author: Author.fromApi(replyData.author),
            }));
        };

        let onClickCancelReply = (e: React.MouseEvent) => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                newReply: '',
            }));
        }

        let replies = [];
        for (const replyId in comment.replies) {
            const reply = comment.replies[replyId];
            replies.push(<CommentReplyComponent key={reply.localId} store={store} api={api} comment={comment} reply={reply} />);
        }

        let replyActions = <></>;
        if (comment.isFocused && comment.newReply.length > 0) {
            replyActions = <div className="comment__reply-actions">
                <button onClick={onClickSendReply}>Send Reply</button>
                <button onClick={onClickCancelReply}>Cancel</button>
            </div>;
        }

        let replyTextarea = <></>;
        if (comment.isFocused || comment.newReply) {
            replyTextarea = <textarea className="comment__reply-input" placeholder="Write a comment back" value={comment.newReply} onChange={onChangeNewReply} style={{resize: 'none'}} />;
        }

        return <>
            <ul className="comment__replies">
                {replies}
            </ul>
            {replyTextarea}
            {replyActions}
        </>;
    }

    renderCreating() {
        let { comment, store, api } = this.props;

        let onChangeText = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                text: e.target.value,
            }));
        };

        let onSave = async (e: React.MouseEvent) => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                mode: 'saving',
            }));

            let commentData = await api.saveComment(comment);

            store.dispatch(updateComment(comment.localId, {
                mode: 'default',
                remoteId: commentData.id,
                author: Author.fromApi(commentData.author),
            }));
        };

        let onCancel = (e: React.MouseEvent) => {
            e.preventDefault();

            store.dispatch(deleteComment(comment.localId));
            comment.annotation.onDelete();
        };

        return <>
            {this.renderHeader()}
            <textarea className="comment__input" value={comment.text} onChange={onChangeText} style={{resize: 'none'}} />
            <div className="comment__edit-actions">
                <button onClick={onSave}>Add Comment</button>
                <button onClick={onCancel}>Cancel</button>
            </div>
        </>;
    }

    renderEditing() {
        let { comment, store, api } = this.props;

        let onChangeText = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                text: e.target.value,
            }));
        };

        let onSave = async (e: React.MouseEvent) => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                mode: 'saving',
            }));

            await api.saveComment(comment);

            store.dispatch(updateComment(comment.localId, {
                mode: 'default',
            }));
        };

        let onCancel = (e: React.MouseEvent) => {
            e.preventDefault();

            comment.annotation.onDelete();
            store.dispatch(updateComment(comment.localId, {
                mode: 'default',
                text: comment.editPreviousText,
            }));
        };

        return <>
            {this.renderHeader()}
            <textarea className="comment__input" value={comment.text} onChange={onChangeText} style={{resize: 'none'}} />
            <div className="comment__edit-actions">
                <button onClick={onSave}>Save</button>
                <button onClick={onCancel}>Cancel</button>
            </div>
            {this.renderReplies()}
        </>;
    }

    renderSaving() {
        let { comment } = this.props;

        return <>
            {this.renderHeader()}
            <textarea className="comment__input" value={comment.text} style={{resize: 'none'}} />
            <div className="comment__edit-actions">
                <p>Saving...</p>
            </div>
            {this.renderReplies()}
        </>;
    }

    renderDeleting() {
        let { comment } = this.props;

        return <>
            {this.renderHeader()}
            <p className="comment__text">{comment.text}</p>
            <div className="comment__edit-actions">
                <p>Deleting...</p>
            </div>
            {this.renderReplies()}
        </>;
    }

    renderDefault() {
        let { comment, store, api } = this.props;

        let onClickEdit = async (e: React.MouseEvent) => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                mode: 'editing',
                editPreviousText: comment.text,
            }));
        };

        let onClickDelete = async (e: React.MouseEvent) => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                mode: 'deleting',
            }));

            await api.deleteComment(comment);

            store.dispatch(deleteComment(comment.localId));
            comment.annotation.onDelete();
        };

        return <>
            {this.renderHeader()}
            <p className="comment__text">{comment.text}</p>
            <div className="comment__actions">
                <a href="#" onClick={onClickEdit}>Edit</a>
                <a href="#" onClick={onClickDelete}>Delete</a>
            </div>
            {this.renderReplies()}
        </>;
    }

    render() {
        let inner;

        switch (this.props.comment.mode) {
            case 'creating':
                inner = this.renderCreating();
                break;

            case 'editing':
                inner = this.renderEditing();
                break;

            case 'saving':
                inner = this.renderSaving();
                break;

            case 'deleting':
                inner = this.renderDeleting();
                break;

            default:
                inner = this.renderDefault();
                break;
        }

        let onClick = () => {
            this.props.store.dispatch(
                setFocusedComment(this.props.comment.localId)
            );
        };

        let top = this.props.layout.getCommentPosition(this.props.comment.localId);
        let right = this.props.comment.isFocused ? 50 : 0;
        return <li key={this.props.comment.localId} className="comment" style={{position: 'absolute', top: `${top}px`, right: `${right}px`}} data-comment-id={this.props.comment.localId} onClick={onClick}>
            {inner}
        </li>;
    }

    componentDidMount() {
        let element = ReactDOM.findDOMNode(this);

        if (element instanceof HTMLElement) {
            // If this is a new comment, focus in the edit box
            if (this.props.comment.mode == 'creating') {
                element.querySelector('textarea').focus();
            }

            this.props.layout.setCommentElement(this.props.comment.localId, element);
            this.props.layout.setCommentHeight(this.props.comment.localId, element.offsetHeight);
        }
    }

    componentWillUnmount() {
        this.props.layout.setCommentElement(this.props.comment.localId, null);
    }

    componentDidUpdate() {
        let element = ReactDOM.findDOMNode(this);

        // Keep height up to date so that other comments will be moved out of the way
        if (element instanceof HTMLElement) {
            this.props.layout.setCommentHeight(this.props.comment.localId, element.offsetHeight);
        }
    }
}
