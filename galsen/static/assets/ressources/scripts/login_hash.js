var a;
function pass() {
    if(a==1) {
        document.getElementById('password').type='password';
        document.getElementById('pass-icon').classList='fa fa-eye-slash right';
        a=0;
    }
    else {
        document.getElementById('password').type='text';
        document.getElementById('pass-icon').classList='fa fa-eye right';
        a=1;
    }
}