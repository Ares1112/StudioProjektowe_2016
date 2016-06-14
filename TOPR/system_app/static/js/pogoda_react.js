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
                <WeatherRow key={weather.key} wiatr={weather.wiatr} mgla={weather.mgla} temp={weather.temperatura}
                deszcz={weather.deszcz} lawina={weather.lawina} czas={weather.czas} szlak={weather.szlak}/>
            );
        });
        return (
            <div className="weatherTable">
                <h3>Pogoda na szlakach</h3>
                <table className="table table-hover text-center">
                    <thead>
                    <tr>
                        <th>Szlak</th>
                        <th>Ostatnia aktualizacja</th>
                        <th>Wiatr [stopień]</th>
                        <th>Mgła [stopień]</th>
                        <th>Temperatura [stopień]</th>
                        <th>Deszcz [stopień]</th>
                        <th>Lawina [stopień]</th>
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
                <td>{this.props.szlak }</td>
                <td>{this.props.czas }</td>
                <td>{this.props.wiatr }</td>
                <td>{this.props.mgla }</td>
                <td>{this.props.temp }</td>
                <td>{this.props.deszcz }</td>
                <td>{this.props.lawina }</td>
            </tr>
        );
    }
});

ReactDOM.render(
    <WeatherTable url="/api/get_weather_info/" pollInterval={3000}/>,
    document.getElementById('pogoda')
);