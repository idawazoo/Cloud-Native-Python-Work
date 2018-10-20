export default class TweetList extends React.Component {
    render() {
        return(
            <div>
                <ul className="collection">
                    <li className="collection-item avatar">
                        <i className="material-icons circle red">play_arrow</i>
                        <span className="title">{this.props.tweets[0].ids}</span>
                        <p>{this.props.tweets[0].name}</p>
                        <p>{this.props.tweets[0].body}</p>
                    </li>
                </ul>
            </div>
        )
    }
}
