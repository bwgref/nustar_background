PRO struct_add_field, struct, tag, data, before=before, after=after $
                    , itag=itag
;Add a new field to an existing structure. If the field already
;exists,
; the data will be copied into the existing field. Keyword may be used
; to control placement of a new field in the structure.
;
;Inputs:
; tag (string) Case insensitive name for the new structure
; field. Leading
;  and trailing spaces will be ignored. If the requested field already
;  exists, the specified data are copied into the existing field.
; data (any) Data used to fill the new or existing field specified in
; tag.
;  The dimensionality of data must agree with the dimensionality of
;  struct,
;  except that scalar data will be replicated into a vector structure,
;  if
;  necessary.
; [before=] (string) The new structure field will be created
; immediately
;  before the first occurence of an existing structure field with the
;  tag
;  name specified by this keyword. An error occurs if the specified
;  tag
;  name does not already exist.
; [after=] (string) The new structure field will be created
; immediately
;  after the first occurence of an existing structure field with the
;  tag
;  name specified by this keyword. An error occurs if the specified
;  tag
;  name does not already exist.
; [itag=] (scalar) The new structure field will be created in position
;  itag, where itag=0 indicates that the new field should be created
;  at
;  the beginning of the structure, itag=1 indicates that the new field
;  should be the second field in the structure, etc.
;
;Input/Output:
; struct (structure) structure to be modified.
;
;Examples:
;
; Add wavelength vector to structure:
;
;   IDL> struct_add_field, sme, 'wave', wave
;
; Add integer mask vector to structure, setting each entry to 1.
;
;   IDL> struct_add_field, sme, 'mask', 1
;
;History:
; 2003-Aug-11 Valenti  Adapted from struct_delete_field.pro.
; 2003-Oct-23 Valenti  Allow new field to be a structure with no
; nesting.

IF n_params() LT 3 THEN BEGIN
  print, 'syntax: struct_add_field, struct, tag, data [begin=, after=, itag=]'
  return
ENDIF

;Check that input is a structure.
  IF size(struct, /tname) NE 'STRUCT' THEN BEGIN
    message, 'first argument is not a structure'
 ENDIF

;Check that no more than one of before=, after=, and itag= are set.
  IF keyword_set(before) + keyword_set(after) $
                         + n_elements(itag) GT 1 THEN BEGIN
    message, 'specify no more than one of before=, after=, and itag='
 ENDIF

;Check dimensionality of data.
  nstruct = n_elements(struct)
  ndata = n_elements(data)
  IF ndata NE 1 AND ndata NE nstruct THEN BEGIN
    message, 'dimensionality of struct and data are incompatible'
 ENDIF

;Get list of structure tags.
  tags = tag_names(struct)
  ntags = n_elements(tags)

;Check whether the requested field exists in input structure.
  ctag = strupcase(strtrim(tag, 2));canoncial form of tag
  imatch = where(tags EQ ctag, nmatch)
  IF nmatch GT 0 THEN BEGIN
     struct.(imatch[0]) = data;overwrite data
    return
 ENDIF

;Figure out where to place the new tag.
  IF n_elements(itag) EQ 0 THEN itag = ntags;end of structure is default
  IF keyword_set(before) THEN BEGIN
    iwhr = where(tags EQ before, nwhr)
    IF nwhr EQ 0 THEN message, 'before=' + before + ' tag not in structure'
    itag = iwhr[0]
 ENDIF
  IF keyword_set(after) THEN BEGIN
    iwhr = where(tags EQ after, nwhr)
    IF nwhr EQ 0 THEN message, 'after=' + after + ' tag not in structure'
    itag = iwhr[0] + 1
 ENDIF

;Use first record as a template for new structure fields.
  rec = struct[0]

;Copy any fields that precede target for new field. Append new field.
  IF itag GT 0 THEN BEGIN;target field occurs first
     new = create_struct(tags[0], rec.(0));initialize structure
     FOR i=1, itag-1 DO BEGIN;insert leading unchange
      new = create_struct(new, tags[i], rec.(i))
   ENDFOR
     new = create_struct(new, tag, data[0]);add new field
  ENDIF ELSE BEGIN
     new = create_struct(tag, data[0]);start with new field
  ENDELSE

;Replicate remainder of structure after desired tag.
  FOR i=itag, ntags-1 DO BEGIN
    new = create_struct(new, tags[i], rec.(i))
 ENDFOR

;Handle trivial case when structure array contains only one element.
  IF nstruct EQ 1 THEN BEGIN
    struct = new
    return
 ENDIF

;Create vector structure to match original dimensionality.
  new = replicate(new, nstruct)

;Copy data into vector structure.
  FOR i=0, itag-1 DO new.(i) = struct.(i)
  IF size(data, /tname) EQ 'STRUCT' THEN BEGIN
    FOR j=0, n_tags(data)-1 DO new.(i).(j) = data.(j)
 ENDIF ELSE BEGIN
    new.(i) = data
 ENDELSE
  FOR i=itag, ntags-1 DO new.(i+1) = struct.(i)
  struct = new

end
