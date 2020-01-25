import Model from "./Model";
import axios from "axios";

export default class User extends Model {
    static endpoints = {
        "login": "Login",
        "register": "Register",
        "refreshtoken": "RefreshToken",
        "logout": "Logout/Access",
        "account": "Account"
    };

    static standardroute = User.endpoints["account"]

    static login(params) {
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${this.endpoints["login"]}`,
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

    static register(params = {}) {
        return new Promise((resolve, reject) => {
            axios.post(`/Api/V1/${this.endpoints["register"]}`, params)
                .then(response => {
                    const model = {"data": response.data};
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                }).finally(() => {
                this.loading = false;
            });
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
        return new Promise((resolve, reject) => {
            axios.post(`/Api/V1/${this.endpoints["logout"]}`)
                .then(response => {
                    const model = {"data": response.data};
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }

    static userupdate(params){
        return new Promise((resolve, reject) => {
            axios.put('/Api/V1/Account', params)
                .then(response => {
                    const model = {"data": response.data};
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }
}