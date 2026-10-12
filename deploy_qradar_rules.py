def run_aql_search(aql_template):
    aql = build_aql(aql_template)
    print(f"   AQL gonderilir...")
    print(f"   {aql[:150]}...")

    # URL-ə query parameter kimi əlavə edirik və https:// qeyd edirik
    url = f"https://{QRADAR_HOST}/api/ariel/searches"
    
    params = {
        'query_expression': aql
    }

    r = requests.post(
        url,
        headers=HEADERS,
        params=params, # query parameter olaraq gedir
        verify=False
    )

    if r.status_code not in [200, 201]:
        print(f"   XETA: HTTP {r.status_code}")
        print(f"   {r.text[:300]}")
        return None

    search_id = r.json().get('search_id')
    print(f"   Search ID: {search_id}")

    for i in range(20):
        time.sleep(3)
        sr = requests.get(
            f'https://{QRADAR_HOST}/api/ariel/searches/{search_id}',
            headers=HEADERS,
            verify=False
        )
        status = sr.json().get('status')
        print(f"   Status [{i+1}]: {status}")
        if status == 'COMPLETED':
            break
        elif status == 'ERROR':
            print("   XETA: AQL icra xetasi")
            return None

    rr = requests.get(
        f'https://{QRADAR_HOST}/api/ariel/searches/{search_id}/results',
        headers=HEADERS,
        verify=False
    )

    if rr.status_code == 200:
        events = rr.json().get('events', [])
        print(f"   {len(events)} event tapildi")
        return events

    print(f"   XETA: Neticeler alinmadi HTTP {rr.status_code}")
    return None
