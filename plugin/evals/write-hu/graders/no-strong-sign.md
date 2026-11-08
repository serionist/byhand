---
type: regex
pattern: 'nyelvi ?modellként|mesterséges intelligenciaként|MI-ként|\[attached_file|oaicite|^\W*(?:természetesen|persze|szívesen)[!,.]+\s*íme'
flags: im
match: not_contains
target: last_message
---
