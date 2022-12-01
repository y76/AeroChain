import Sdk, { ManifestBuilder } from '@radixdlt/alphanet-walletextension-sdk'
import { StateApi, TransactionApi } from '@radixdlt/alphanet-gateway-api-v0-sdk'

const sdk = Sdk()
const transactionApi = new TransactionApi()
const stateApi = new StateApi()