import Model from "./Model";
import axios from "axios";

export default class User extends Model {
    static endpoints = {
        "login": "Login",
        "register": "Register",
        "refreshtoken": "RefreshToken",
        "logout": ["Logout/Refresh", "Logout/Access"],
        "account": "Account"
    };

    static login(params) {
        return new Promise((resolve, reject) => {
            axios.post(`/Api/V1/${this.endpoints["login"]}`,
                {
                    params: params,
                })
                .then(response => {
                    const model = {"data": response.data};
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }

    static register(params) {
        return new Promise((resolve, reject) => {
            axios.post(`/Api/V1/${this.endpoints["register"]}`,
                {
                    params: params,
                })
                .then(response => {
                    const model = {"data": response.data};
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }

    static refreshtoken(params) {
        return new Promise((resolve, reject) => {
            axios.post(`/Api/V1/${this.endpoints["refreshtoken"]}`,
                {
                    params: params,
                })
                .then(response => {
                    const model = {"data": response.data};
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }

    static logout() {
        let return_json = {}
        let refresh = Promise((resolve, reject) => {
            axios.post(`/Api/V1/${this.endpoints["logout"][0]}`)
                .then(response => {
                    const model = {"data": response.data};
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });

        let access = Promise((resolve, reject) => {
            axios.post(`/Api/V1/${this.endpoints["logout"][1]}`)
                .then(response => {
                    const model = {"data": response.data};
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
        return new Promise.all([refresh, access]).then(data => {
            return_json["refresh"] = data
        }).then(data => {
            return_json["access"] = data
            return return_json
        });
    }

    constructor() {
        super(User.endpoints["account"]);
    }
}