from typing import NamedTuple, Any, Optional
from uuid import uuid4


class NotePitch(NamedTuple):
    step: str
    octave: int
    alter: int = 0

    @classmethod
    def from_music_xml_note_pitch(self, music_xml_note_pitch):
        return NotePitch(
            step=music_xml_note_pitch.get('step'),
            octave=int(music_xml_note_pitch.get('octave')),
            alter=int(music_xml_note_pitch.get('alter', 0))
        )


class NoteDisplayParams(NamedTuple):
    stem: Optional[str]
    beam: Optional[Any]

    @classmethod
    def from_music_xml_note(self, music_xml_note):
        return NoteDisplayParams(
            stem=music_xml_note.get('stem'),
            beam=music_xml_note.get('beam')
        )


class Note(NamedTuple):
    id: Any
    staff: Any
    voice: Any
    pitch: Any
    rest: Any
    chord: Any
    type: Any
    dot: Any
    name: Any
    time_modification: Any  # TODO make type
    display: NoteDisplayParams
    notations: Any  # TODO make type

    @classmethod
    def from_music_xml_note(self, music_xml_note):
        is_rest_note = False if music_xml_note.get('rest', 'nope') == 'nope' else True
        is_dotted_note = False if music_xml_note.get('dot', 'nope') == 'nope' else True
        is_chord_note = False if music_xml_note.get('chord', 'nope') == 'nope' else True
        pitch = None if is_rest_note else NotePitch.from_music_xml_note_pitch(music_xml_note.get('pitch'))
        note_name = 'rest' if is_rest_note else '{}{}{}'.format(
            pitch.step,
            pitch.octave,
            ['', '#', 'b'][int(pitch.alter)]
        )
        staff = music_xml_note.get('staff', None)
        return Note(
            id = str(uuid4()),
            staff=int(staff) if staff else 1,  # for instruments with multiple staffs
            voice=int(music_xml_note.get('voice')),  # optional division
            rest=is_rest_note,
            chord=is_chord_note,
            pitch=pitch,
            type=music_xml_note.get('type'),
            dot=is_dotted_note,
            name=note_name,
            time_modification=music_xml_note.get('time-modification'),
            display=NoteDisplayParams.from_music_xml_note(music_xml_note),
            notations=music_xml_note.get('notations'),
        )
