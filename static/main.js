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
            },
            {
                'ids' : 2, 
                'name': 'guest', 
                'body': '"whatever." - Paulo Coelho #Motivation'
            }            
        ]}
    }

    /*
    addTweet(tweet) {
        let newTweet = this.state.tweets;
        newTweet.unshift({
                'id': Date.now(),
                'name': 'guest',
                'body': tweet
            })
        this.setState({
            tweets: newTweet
        })
    }
    */

    addTweet(tweet) {
        var self = this;
        $.ajax({
            url: '/api/v2/tweets',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify({
                'username': "idawazoo",
                'body': tweet,
            }),
            success: function(data) {
                return console.log("success");
            },
            error: function() {
                return console.log("Failed");
            }
        });
    }

    componentDidMount() {
        var self = this;
        $.ajax({
            url: '/api/v2/tweets',
            success: function(data) {
                self.setState({
                    tweets: JSON.parse(data)
                })
                alert(self.state.tweets);
                return console.log("success");
            },
            error: function() {
                return console.log("Failed");
            }
        });
    }

    render() {
        return (
            <div>
                <Tweet sendTweet={this.addTweet.bind(this)} />
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