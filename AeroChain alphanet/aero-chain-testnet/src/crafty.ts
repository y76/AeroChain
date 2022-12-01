import Sdk, { ManifestBuilder } from '@radixdlt/alphanet-walletextension-sdk';
import { StateApi, TransactionApi } from '@radixdlt/alphanet-gateway-api-v0-sdk'

// Initialize the SDK
const sdk = Sdk()
const transactionApi = new TransactionApi()
const stateApi = new StateApi()

// Global states
let accountAddress: string // User account address
let componentAddress: string  // GumballMachine component address
let resourceAddress: string // GUM resource address
/*
document.getElementById('fetchAccountAddress').onclick = async function () {
  // Retrieve extension user account address
  const result = await sdk.request({
    accountAddresses: {},
  })

  if (result.isErr()) {
    throw result.error
  }

  const { accountAddresses } = result.value
  if (!accountAddresses) return

  document.getElementById('accountAddress').innerText = accountAddresses[0].address
  accountAddress = accountAddresses[0].address
}
*//*
document.getElementById('instantiateComponent').onclick = async function () {
  let packageAddress = document.getElementById("packageAddress").value;
  
  let manifest = new ManifestBuilder()
    .callMethod(accountAddress, "lock_fee", ['Decimal("100")'])
    .callFunction(packageAddress, "DoNotFly", "instantiate_list", ['Decimal("100")'])
    //.callMethod(accountAddress, "lock_fee", ['Decimal("100")'])
    //.callFunction(packageAddress, "GumballMachine", "instantiate_gumball_machine", ['Decimal("10")'])
    .build()
    .toString();

    console.log(manifest)
  // Send manifest to extension for signing
  const hash = await sdk
    .sendTransaction(manifest)
    .map((response) => response.transactionHash)
    console.log(manifest)
  if (hash.isErr()) throw hash.error

  // Fetch the receipt from the Gateway SDK
  const receipt = await transactionApi.transactionReceiptPost({
    v0CommittedTransactionRequest: { intent_hash: hash.value },
  })
  console.log(receipt)

  componentAddress = receipt.committed.receipt.state_updates.new_global_entities[4].global_address
  document.getElementById('componentAddress').innerText = componentAddress;
  
  resourceAddress = receipt.committed.receipt.state_updates.new_global_entities[0].global_address
  document.getElementById('gumAddress').innerText = resourceAddress;
}*/

document.getElementById('confirm').onclick = async function () {
  let packageAddress: string

  const result = await sdk.request({
    accountAddresses: {},
  })

  if (result.isErr()) {
    throw result.error
  }

  const { accountAddresses } = result.value
  if (!accountAddresses) return

  accountAddress = accountAddresses[0].address
  componentAddress = "component_tdx_a_1qf9fpatfymgpy7nchzmn7txk9avm04f3mw7fy2hvq2gsyvfmqf"
  packageAddress = "package_tdx_a_1q8md97w7r0tnnkcvwee034g5rxekg5x0zsjyl9y7c29shvwte9"

  const queryString = window.location.search;
  console.log(queryString);
  const urlParams = new URLSearchParams(queryString);
  const FirstName = urlParams.get('FirstName')
  const LastName = urlParams.get('LastName')
  const BirthDate = urlParams.get('BirthDate')
  const Reason = urlParams.get('Reason')
  console.log(FirstName)
  console.log(LastName)
  console.log(BirthDate)
  console.log(Reason)

  let publishString: string
  publishString = "\""+FirstName+"\""+"\""+LastName+"\""+"\""+Reason+"\""+"\""+BirthDate+"\""
  console.log(publishString)
  let manifest = new ManifestBuilder()

    .callMethod(accountAddress, "lock_fee", ['Decimal("10")'])
    .callMethod(componentAddress, "mint_nft", [publishString])
    .build()
    .toString();

    console.log(manifest)
  // Send manifest to extension for signing
  const hash = await sdk
    .sendTransaction(manifest)
    .map((response) => response.transactionHash)
    console.log(manifest)
  if (hash.isErr()) throw hash.error
  console.log(manifest)
  // Fetch the receipt from the Gateway SDK
  const receipt = await transactionApi.transactionReceiptPost({
    v0CommittedTransactionRequest: { intent_hash: hash.value },
  })
  console.log(receipt)
  // Show the receipt on the DOM
  window.location.replace("http://127.0.0.1:8000/AeroChain/accepted");
  //document.getElementById('receipt').innerText = JSON.stringify(receipt.committed.receipt, null, 2);
};
/*
document.getElementById('checkBalance').onclick = async function () {

  // Fetch the state of the account component
  const account_state = await stateApi.stateComponentPost({
    v0StateComponentRequest: { component_address: accountAddress }
  })

  let account_gum_vault = account_state.owned_vaults.find(vault => vault.resource_amount.resource_address == `${resourceAddress}`)

  // Fetch the state of the machine component
  const machine_state = await stateApi.stateComponentPost({
    v0StateComponentRequest: { component_address: componentAddress }
  })

  let machine_gum_vault = machine_state.owned_vaults.find(vault => vault.resource_amount.resource_address == `${resourceAddress}`)

  // Update the DOM
  document.getElementById("userBalance").innerText = account_gum_vault.resource_amount.amount_attos / Math.pow(10,18)
  document.getElementById("machineBalance").innerText = machine_gum_vault.resource_amount.amount_attos / Math.pow(10,18)
};*/