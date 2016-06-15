var WeatherTable = React.createClass({
    getInitialState: function () {
        return {data: []};
    },
    componentDidMount: function () {
        this.loadWeatherFromServer();
        setInterval(this.loadWeatherFromServer, this.props.pollInterval);
    },
    loadWeatherFromServer: function () {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function (data) {
                this.setState({data: data});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    render: function () {
        var weatherRows = this.state.data.map(function (weather) {
            return (
                <WeatherRow key={weather.key} telefon={weather.telefon} zagrozenie={weather.zagrozenie}/>
            );
        });
        return (
            <div className="weatherTable">
                <h3>Zagrożeni turyści na szlakach</h3>
                <table className="table table-hover text-center">
                    <thead>
                    <tr>
                        <th>Telefon</th>
                        <th>Zagrożenie</th>
                    </tr>
                    </thead>
                    <tbody>
                    {weatherRows}
                    </tbody>
                </table>
            </div>
        );
    }
});

var WeatherRow = React.createClass({
    render: function () {
        return (
            <tr>
                <td>{this.props.telefon }</td>
                <td>{this.props.zagrozenie }</td>
            </tr>
        );
    }
});

ReactDOM.render(
    <WeatherTable url="/api/get_tourist_danger_info/" pollInterval={3000}/>,
    document.getElementById('tourists')
);