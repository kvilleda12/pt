// BodyParts Enums

export const BodyPartMap = {
    'neck': 'n',
    'chest': 'c',
    'left_shoulder': 'ls',
    'right_shoulder': 'rs',
    'left_tricep': 'lt',
    'right_tricep': 'rt',
    'left_bicep': 'lb',
    'right_bicep': 'rb',
    'abdomen': 'a',
    'back': 'b',
    'left_hamstring': 'lh',
    'right_hamstring': 'rh',
    'left_quad': 'lq',
    'right_quad': 'rq',
    'left_calf': 'lc',
    'right_calf': 'rc',
    'left_ankle': 'la',
    'right_ankle': 'ra',
    'everything': 'e'
};

export type BodyPartKey = keyof typeof BodyPartMap;