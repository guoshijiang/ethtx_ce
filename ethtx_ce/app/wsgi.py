#  Copyright 2021 DAI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os

from ethtx import EthTx, EthTxConfig
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from . import frontend, api

app = Flask(__name__)

ethtx_config = EthTxConfig(
    mongo_connection_string="mongomock://localhost/ethtx",
    etherscan_api_key="W972DC11QYVEWRSWCRYHTT4H362PK43P8N",
    web3nodes={
        "mainnet": {
            "hook": "https://dark-black-meadow.quiknode.pro/bcaa5550a8ecfe4d2c22f5d314cda3c40d129e88",
            "poa": False
        }
    },
    default_chain="mainnet",
    etherscan_urls={
        "mainnet": "https://api.etherscan.io/api",
    },
)

ethtx = EthTx.initialize(ethtx_config)

app.wsgi_app = DispatcherMiddleware(
    frontend.create_app(engine=ethtx, settings_override=EthTxConfig),
    {"/api": api.create_app(engine=ethtx, settings_override=EthTxConfig)},
)

if __name__ == "__main__":
    app.run()
