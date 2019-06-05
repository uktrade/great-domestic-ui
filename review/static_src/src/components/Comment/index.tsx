import * as React from 'react';
import * as ReactDOM from 'react-dom';

import {Comment, CommentReply} from '../../state';
import {updateComment, deleteComment, addReply, updateReply} from '../../actions';
import APIClient from '../../api';
import {LayoutController} from '../../utils/layout';
import {getNextReplyId} from '../../utils/sequences';
import CommentReplyComponent from '../CommentReply';

import './style.scss';

export interface CommentProps {
    store: any,
    comment: Comment,
    api: APIClient,
    layout: LayoutController,
}

export default class CommentComponent extends React.Component<CommentProps> {
    renderHeader() {
        return <div>
            <h2>{this.props.comment.author}</h2>
            <p>DATE</p>
        </div>;
    }

    renderCreating() {
        let { comment, store, api } = this.props;

        let onChangeText = e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                text: e.target.value,
            }));
        };

        let onSave = async e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                mode: 'saving',
            }));

            let commentData = await api.saveComment(comment);

            store.dispatch(updateComment(comment.localId, {
                mode: 'default',
                remoteId: commentData.id,
            }));
        };

        let onCancel = e => {
            e.preventDefault();

            comment.annotation.onDelete();
            store.dispatch(deleteComment(comment.localId));
        };

        return <>
            <h3>New comment</h3>
            <textarea className="comment__input" value={comment.text} onChange={onChangeText} style={{resize: 'none'}} />
            <button onClick={onSave}>Add Comment</button>
            <button onClick={onCancel}>Cancel</button>
        </>;
    }

    renderEditing() {
        let { comment, store, api } = this.props;

        let onChangeText = e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                text: e.target.value,
            }));
        };

        let onSave = async e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                mode: 'saving',
            }));

            await api.saveComment(comment);

            store.dispatch(updateComment(comment.localId, {
                mode: 'default',
            }));
        };

        let onCancel = e => {
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
            <button onClick={onSave}>Save</button>
            <button onClick={onCancel}>Cancel</button>
        </>;
    }

    renderSaving() {
        let { comment } = this.props;

        return <>
            <p>{comment.text}</p>
            <p>Saving...</p>
        </>;
    }

    renderDeleting() {
        let { comment } = this.props;

        return <>
            <p>{comment.text}</p>
            <p>Deleting...</p>
        </>;
    }

    renderDefault() {
        let { comment, store, api } = this.props;

        let onClickEdit = async e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                mode: 'editing',
                editPreviousText: comment.text,
            }));
        };

        let onClickDelete = async e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                mode: 'deleting',
            }));

            await api.deleteComment(comment);

            store.dispatch(deleteComment(comment.localId));
            comment.annotation.onDelete();
        };

        let onChangeNewReply = e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                newReply: e.target.value,
            }));
        };

        let onClickSendReply = async e => {
            e.preventDefault();

            let replyId = getNextReplyId();
            let reply = new CommentReply(replyId, {text: comment.newReply, mode: 'saving'});
            store.dispatch(addReply(comment.localId, reply));

            store.dispatch(updateComment(comment.localId, {
                newReply: '',
            }));

            let replyData = await api.saveCommentReply(comment, reply);

            store.dispatch(updateReply(comment.localId, replyId, {
                remoteId: replyData.id,
                mode: 'default',
            }));
        };

        let onClickCancelReply = e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                newReply: '',
            }));
        }

        let replies = [];
        for (const replyId in comment.replies) {
            const reply = comment.replies[replyId];
            replies.push(<CommentReplyComponent key={reply.localId} store={store} api={api} reply={reply} />);
        }

        let replyActions = <></>;
        if (comment.newReply.length > 0) {
            replyActions = <div className="comment__reply-actions">
                <button onClick={onClickSendReply}>Send Reply</button>
                <button onClick={onClickCancelReply}>Cancel</button>
            </div>;
        }

        return <>
            {this.renderHeader()}
            <p className="comment__text">{comment.text}</p>
            <div className="comment__actions">
                <a href="#" onClick={onClickEdit}>Edit</a>
                <a href="#" onClick={onClickDelete}>Delete</a>
            </div>
            <ul className="comment__replies">
                {replies}
            </ul>
            <textarea className="comment__reply-input" placeholder="Write a comment back" value={comment.newReply} onChange={onChangeNewReply} style={{resize: 'none'}} />
            {replyActions}
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

        let position = this.props.layout.getCommentPosition(this.props.comment.localId);
        return <li key={this.props.comment.localId} className="comment" style={{position: 'absolute', top: `${position}px`}} data-comment-id={this.props.comment.localId}>
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
