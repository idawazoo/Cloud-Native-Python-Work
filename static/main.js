import Tweet from "./components/Tweet";
import TweetList from "./components/TweetList";
import cookie from 'react-cookies';

class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = { userId: cookie.load('session') }; //needs a session
        this.state = { tweets: [
            {
                'ids' : 1, 
                'name': 'guest', 
                'body': '"Listen to your heart. It knows all things." - Paulo Coelho #Motivation'
            }
        ]}
    }

    render() {
        return (
            <div>
                <Tweet />
                <TweetList tweets={this.state.tweets} />
            </div>
        )
    }
}

let documentReady =() => {
    ReactDOM.render(
        <Main />,
            document.getElementById('react')
    );
};

$(documentReady);