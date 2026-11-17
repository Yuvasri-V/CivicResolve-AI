const STORAGE_KEY = "civicresolve_voter_key";

export function getVoterKey() {
  let key = localStorage.getItem(STORAGE_KEY);
  if (!key) {
    key = `voter-${crypto.randomUUID()}`;
    localStorage.setItem(STORAGE_KEY, key);
  }
  return key;
}
