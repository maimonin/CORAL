/*****************************/
/* Predicates Declarations */
/*****************************/
primitive(dataFlow(_pod1, _pod2, _protocol, _port)).
primitive(residesOn(_pod, _software, _version)).
primitive(vulExists(_cveId, _software, _version, _access_vector, _lose_types, _severity)).
primitive(hacl(_source, _pod, _protocol, _port)).

derived(vulnerablePod(_pod)).

meta(attackGoal(_)).

/***********************************************/
/*             Tabling Predicates              */
/*   All derived predicates should be tabled   */
/***********************************************/
:- table vulnerablePod/1.

/**********************/
/* Interaction Rules */
/**********************/
interaction_rule(
  (vulnerablePod(Pod) :-
    hacl('Internet', Pod, _protocol, _port),
    residesOn(Pod, Software, Version),
    vulExists(_cveId, Software, Version, 'Network', _lose_types, _severity)),
  rule_desc('vul. with remote access-vector in a pod that interacts with the Internet', 1.0)).

interaction_rule(
  (vulnerablePod(Pod2) :-
    vulnerablePod(Pod1),
    dataFlow(Pod1, Pod2, _protocol, _port),
    residesOn(Pod2, Software, Version),
    vulExists(_cveId, Software, Version, 'Network', _lose_types, 'CRITICAL')),
  rule_desc('vulnerable pod1 and connection to pod2 with severe CVE lead to vul. in pod2', 1.0)).
