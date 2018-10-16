export default class Tweet extends React.Component {
    render() {
        return(
            <div className="row">
            <nav/>
            <form>
                <div>
                    <textarea ref="tweetTextArea" />
                    <label>How you doing?</label>
                    <button>Tweet now</button>
                </div>
            </form>
            </div>
        );
    }
}