

(define (problem BW-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b5)
(on b3 b1)
(on-table b4)
(on b5 b7)
(on b6 b3)
(on-table b7)
(clear b4)
(clear b6)
)
(:goal
(and
(on b3 b1)
(on b4 b7)
(on b5 b6)
(on b6 b2)
(on b7 b5))
)
)


