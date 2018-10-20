export default class Tweettemplate extends React.Component {
    render(props) {
        return (
            <li className="collection-item avatar">
                <i className="materia-icons circle read">play_arrow</i>
                <span className="title">{this.props.tweetedby}</span>
                <p>{this.props.body}</p>
                <p>{this.props.timestamp}</p>
            </li>
        );
    }
}
