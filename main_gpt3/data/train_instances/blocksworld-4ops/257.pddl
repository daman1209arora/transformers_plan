

(define (problem BW-rand-8)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b1)
(on-table b4)
(on b5 b7)
(on b6 b8)
(on b7 b3)
(on b8 b5)
(clear b2)
(clear b4)
(clear b6)
)
(:goal
(and
(on b1 b4)
(on b2 b5)
(on b4 b6)
(on b7 b3)
(on b8 b7))
)
)


