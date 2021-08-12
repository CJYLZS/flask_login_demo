
const { Component } = React
class EntryPage extends Component {
    constructor(props) {
        super(props)
        this.state = {
            current_view: document.getElementById('default_view').value,
            username: "",
            passwd: "",
            vcode: "",
            email: ""
        }
    }
    reset_input = () => {
        let id_list = ['username', 'password', 'email', 'vcode'];
        id_list.forEach(item => {
            let elem = document.getElementById(item);
            if(elem){
                elem.value = '';
            }
        });
    }
    submit_login = () => {
        console.log('click login button!');
        if (this.state.username && this.state.passwd) {
            fetch('/login', {
                method: 'POST',
                body: JSON.stringify({
                    'username': this.state.username,
                    'password': this.state.passwd
                }),
                headers: new Headers({
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.getElementById('csrf_token').value
                })
            })
                .then(res => res.json())
                .then(res => {
                    if (res.result) {
                        window.location = res.url;
                    } else {
                        alert(res.msg);
                        if(res.url.length > 0){
                            window.location = res.url;
                        }
                    }
                })
        }
    }
    submit_signin = () => {
        console.log('click signup button!');
        if (this.state.username && this.state.passwd && this.state.email && this.state.vcode) {
            fetch('/signup', {
                method: 'POST',
                body: JSON.stringify({
                    'username': this.state.username,
                    'password': this.state.passwd,
                    'email': this.state.email,
                    'vcode': this.state.vcode
                }),
                headers: new Headers({
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.getElementById('csrf_token').value
                })
            })
                .then(res => res.json())
                .then(res => {
                    if (res.result) {
                        window.location = res.url;
                    } else {
                        this.get_new_vcode();
                        alert(res.msg);
                    }
                });
        } else {
            alert('请填写完整信息!');
        }
    }
    set_new_password = () => {
        console.log('click signup button!');
        if (this.state.passwd && this.state.vcode) {
            let old_hash = '';
            let args_name = 'old_hash'
            let reg = new RegExp("(^|&)" + args_name + "=([^&]*)(&|$)", "i");
            let r = window.location.search.substr(1).match(reg);
            if(r != null){
                old_hash = decodeURIComponent(r[2]);
            }
            fetch('/pwset', {
                method: 'POST',
                body: JSON.stringify({
                    'password': this.state.passwd,
                    'old_hash': old_hash,
                    'vcode': this.state.vcode
                }),
                headers: new Headers({
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.getElementById('csrf_token').value
                })
            })
                .then(res => res.json())
                .then(res => {
                    if (res.result) {
                        window.location = res.url;
                    } else {
                        this.get_new_vcode();
                        alert(res.msg);
                    }
                });
        } else {
            alert('请填写完整信息!');
        }
    }
    send_reset_link = () => {
        console.log('click reset button!');
        if (this.state.email && this.state.vcode) {
            fetch('/pwreset', {
                method: 'POST',
                body: JSON.stringify({
                    'email': this.state.email,
                    'vcode': this.state.vcode
                }),
                headers: new Headers({
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.getElementById('csrf_token').value
                })
            })
                .then(res => res.json())
                .then(res => {
                    
                    if(res.result){
                        alert(res.msg);
                    }else{
                        this.get_new_vcode();
                        alert(res.msg);
                    }
                });
        } else {
            alert('请填写完整信息!');
        }
    }
    get_new_vcode = () => {
        console.log('click vcode img!');
        fetch('/newvcode', {
            method: 'GET',
            headers: new Headers({
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementById('csrf_token').value
            })
        })
            .then(res => res.json())
            .then(res => {
                let ele = document.getElementById('vcode_img');
                ele.src = res.url;
                document.getElementById('vcode_url').value = ele.src;
            });
    }
    verify_vcode = () => {
        console.log('click OK button!');
        if (this.state.vcode) {
            fetch('/captcha', {
                method: 'POST',
                body: JSON.stringify({
                    'vcode': this.state.vcode
                }),
                headers: new Headers({
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.getElementById('csrf_token').value
                })
            })
                .then(res => res.json())
                .then(res => {
                    if(res.result){
                        window.location = res.url;
                    }else{
                        alert(res.msg);
                    }
                    
                });
        } else {
            alert('请填写完整信息!');
        }
    }
    
    change_view = (view) => {
        this.setState({
            current_view: view
        });
        this.reset_input();
    }
    user_change = (e) => {
        this.setState({
            username: e.target.value
        });
    }
    passwd_change = (e) => {
        this.setState({
            passwd: e.target.value
        });
    }
    email_change = (e) => {
        this.setState({
            email: e.target.value
        });
    }
    vcode_change = (e) => {
        this.setState({
            vcode: e.target.value
        })
    }

    current_view = () => {
        switch (this.state.current_view) {
            case "signUp":
                return (
                    <form>
                        <h2>Sign Up!</h2>
                        <fieldset>
                            <legend>Create Account</legend>
                            <ul>
                                <li>
                                    <label htmlFor="email">Email:</label>
                                    <input type="email" id="email" onChange={this.email_change} required />
                                </li>
                                <li>
                                    <label htmlFor="username">Username:</label>
                                    <input type="text" id="username" onChange={this.user_change} required />
                                </li>
                                <li>
                                    <label htmlFor="password">Password:</label>
                                    <input type="password" id="password" onChange={this.passwd_change} required />
                                </li>
                                <li>
                                    <label htmlFor="v_picture">VCode:</label>
                                    <img id="vcode_img" src = {document.getElementById('vcode_url').value} onClick = {this.get_new_vcode}></img>
                                </li>
                                <li>
                                    <label htmlFor="vcode">VCode:</label>
                                    <input type="vcode" id="vcode" onChange={this.vcode_change} required />
                                </li>
                            </ul>
                        </fieldset>
                        <button type="button" onClick={this.submit_signin}>Submit</button>
                        <button type="button" onClick={() => this.change_view("logIn")}>Have an Account?</button>
                    </form>
                );
            case "logIn":
                return (
                    <form method='POST'>
                        <h2>Welcome Back!</h2>
                        <fieldset>
                            <legend>Log In</legend>
                            <ul>
                                <li>
                                    <label htmlFor="username">Username:</label>
                                    <input type="text" id="username" onChange={this.user_change} required />
                                </li>
                                <li>
                                    <label htmlFor="password">Password:</label>
                                    <input type="password" id="password" onChange={this.passwd_change} required />
                                </li>
                                <li>
                                    <i />
                                    <a onClick={() => this.change_view("PWReset")} href="#">Forgot Password?</a>
                                </li>
                            </ul>
                        </fieldset>
                        <button type="button" onClick={this.submit_login}>Login</button>
                        <button type="button" onClick={() => this.change_view("signUp")}>Create an Account</button>
                    </form>
                );
            case "PWReset":
                return (
                    <form>
                        <h2>Reset Password</h2>
                        <fieldset>
                            <legend>Password Reset</legend>
                            <ul>
                                <li>
                                    <em>New Random Password will be send to you mailbox</em>
                                </li>
                                <li>
                                    <label htmlFor="email">Email:</label>
                                    <input type="email" id="email" onChange={this.email_change} required />
                                </li>
                                <li>
                                    <label htmlFor="v_picture">VCode:</label>
                                    <img id="vcode_img" src = {document.getElementById('vcode_url').value} onClick = {this.get_new_vcode}></img>
                                </li>
                                <li>
                                    <label htmlFor="vcode">VCode:</label>
                                    <input type="vcode" id="vcode" onChange={this.vcode_change} required />
                                </li>
                            </ul>
                        </fieldset>
                        <button type="button" onClick={this.send_reset_link}>Send Reset Link</button>
                        <button type="button" onClick={() => this.change_view("logIn")}>Back To Login</button>
                    </form>
                );
            case "PWSet":
                return (
                    <form>
                        <h2>Set Your New Password</h2>
                        <fieldset>
                            <legend>Password Set</legend>
                            <ul>
                                <li>
                                    <em>Typein New Password</em>
                                </li>
                                <li>
                                    <label htmlFor="password">Password:</label>
                                    <input type="password" id="password" onChange={this.passwd_change} required />
                                </li>
                                <li>
                                    <label htmlFor="v_picture">VCode:</label>
                                    <img id="vcode_img" src = {document.getElementById('vcode_url').value} onClick = {this.get_new_vcode}></img>
                                </li>
                                <li>
                                    <label htmlFor="vcode">VCode:</label>
                                    <input type="vcode" id="vcode" onChange={this.vcode_change} required />
                                </li>
                            </ul>
                        </fieldset>
                        <button type="button" onClick={this.set_new_password}>OK</button>
                    </form>
                );
            case "Captcha":
                return (
                    <form>
                        <h2>Are You Robot?</h2>
                        <fieldset>
                            <legend>Verify</legend>
                            <ul>
                                <li>
                                    <em>Typein Verify Code Click Image To Change New Image</em>
                                </li>
                                <li>
                                    <label htmlFor="v_picture">VCode:</label>
                                    <img id="vcode_img" src = {document.getElementById('vcode_url').value} onClick = {this.get_new_vcode}></img>
                                </li>
                                <li>
                                    <label htmlFor="vcode">VCode:</label>
                                    <input type="vcode" id="vcode" onChange={this.vcode_change} required />
                                </li>
                            </ul>
                        </fieldset>
                        <button type="button" onClick={this.verify_vcode}>OK</button>
                    </form>
                );
            default:
                break
        }
    }

    render = () => {
        return (
            <section id="entry-page">
                {this.current_view()}
            </section>
        )
    }
}

ReactDOM.render(<EntryPage />, document.getElementById("app"))

function check_err() {
    let err_msg = document.getElementById('err_msg').value;
    if (err_msg.length != 0) {
        alert(err_msg);
    }
}
check_err();