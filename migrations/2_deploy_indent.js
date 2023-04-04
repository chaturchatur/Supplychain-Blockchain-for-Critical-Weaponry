var Indent = artifacts.require("Indent");

module.exports = function(deployer) {
    deployer.deploy(Indent,true);
};